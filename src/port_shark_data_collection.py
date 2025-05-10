import subprocess
import re
import pyshark
import csv
from datetime import datetime
import time

def get_pid_ports(pid):
    # Retrieve the ports associated with the given PID
    result = subprocess.run(
        ["lsof", "-i", "-a", f"-p{pid}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    output = result.stdout
    ports = set()
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+):(\d+)->')

    # Extract the ports from the lsof output
    for line in output.splitlines():
        match = pattern.search(line)
        if match:
            ports.add(match.group(2))

    return list(ports)

def build_display_filter(ports):
    # Build the display filter for PyShark to capture traffic based on ports
    return ' || '.join([f'tcp.dstport == {port}' for port in ports])

def main():
    pid = input("Enter the PID of the process to capture traffic for: ")
    
    try:
        pid = int(pid)
    except ValueError:
        print("Invalid PID. Please enter a valid integer.")
        return

    pid_ports = get_pid_ports(pid)
    if not pid_ports:
        print(f"No ports found for PID {pid}.")
        return

    display_filter = build_display_filter(pid_ports)
    print(f"Capturing traffic for PID {pid} on ports: {pid_ports}")
    
    capture_duration = 60  # Duration to run the capture in seconds (e.g., 60 seconds)
    capture = pyshark.LiveCapture(interface='en0', display_filter=display_filter)
    
    output_file = f'pid_{pid}_packet_log.csv'
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Source IP', 'Destination IP', 'Protocol', 'Length'])

        print(f"Capturing packets for {capture_duration} seconds... Press CTRL+C to stop.\n")
        start_time = time.time()
        try:
            for packet in capture.sniff_continuously():
                # Stop capturing once the duration has passed
                if time.time() - start_time > capture_duration:
                    break
                try:
                    writer.writerow([
                        packet.sniff_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        packet.ip.src,
                        packet.ip.dst,
                        packet.highest_layer,
                        packet.length
                    ])
                except AttributeError:
                    continue
        except KeyboardInterrupt:
            print("Capture stopped by user.")
        except EOFError:
            print("Capture ended unexpectedly (EOFError).")
        finally:
            capture.close()

if __name__ == "__main__":
    main()
