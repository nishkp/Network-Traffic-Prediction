import subprocess
import csv
import re
from datetime import datetime
import time

output_file = 'packet_log.csv'

def parse_tcpdump_output(line):
    match = re.match(r'(\d+\.\d+)\s+IP\s+([\d\.]+)\.(\d+)\s+>\s+([\d\.]+)\.(\d+):\s+(\S+)\s+length\s+(\d+)', line)
    
    if match:
        timestamp = match.group(1)
        src_ip = match.group(2)
        dst_ip = match.group(4)
        protocol = match.group(6)
        length = match.group(7)
        
        timestamp = datetime.utcfromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S.%f')

        return [timestamp, src_ip, dst_ip, protocol, length]
    
    print(f"Regex did not match line: {line}")
    return None

tcpdump_command = [
    'sudo', 'tcpdump', '-i', 'en0', '-nn', '-tttt', 'tcp'
]

start_time = time.time()
capture_duration = 10

try:
    with subprocess.Popen(tcpdump_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        print(f"Capturing packets for {capture_duration} seconds... Press CTRL+C to stop.\n")
        
        while time.time() - start_time < capture_duration:
            line = process.stdout.readline()
            if line:
                print(f"Line from tcpdump: {line}")
                parsed_data = parse_tcpdump_output(line)
                if parsed_data:
                    with open(output_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(parsed_data)
                    print(f"Parsed Data: {parsed_data}")
            else:
                break

except KeyboardInterrupt:
    print("Capture stopped.")
except Exception as e:
    print(f"Error: {e}")

print("Capture completed.")
