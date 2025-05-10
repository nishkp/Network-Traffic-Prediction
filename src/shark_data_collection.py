import pyshark
import csv
from datetime import datetime
import subprocess
import re
import os


capture = pyshark.LiveCapture(interface='en0', display_filter='http || tls')

output_file = 'packet_log.csv'
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Source IP', 'Destination IP', 'Protocol', 'Length'])

    print(f"Capturing packets... Press CTRL+C to stop.\n")
    try:
        for packet in capture.sniff_continuously():
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
        print("Capture stopped.")


