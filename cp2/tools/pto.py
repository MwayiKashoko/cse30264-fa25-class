import sys
import subprocess
import os

def prune(pcap_file):
    #Path to find-tcp-max.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    find_tcp_max_path = os.path.join(script_dir, 'find-tcp-max.py')
    
    #Run find-tcp-max.py to compute snaplen
    #Had to use Stackoverflow to see how to run command line functions in Python
    result = subprocess.run(
        [sys.executable, find_tcp_max_path, pcap_file],
        capture_output=True, text=True, check=True
    )

    max_header_len = int(result.stdout.strip())

    base_name = os.path.basename(pcap_file)
    output_file = f"pto-{base_name}"

    #-r read file, -w write to file, -s snapshot length
    #Also used Stackoverflow to figure out how to use tshark since pyshar.FileCapture was running slowly and taking up ~10gb of memory
    subprocess.run([
        'tshark',
        '-r', pcap_file,
        '-w', output_file,
        '-s', str(max_header_len)
    ], check=True)

    print(f"Successfully pruned capture and saved as: {output_file} with (snaplen={max_header_len})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pto.py <pcap_file>")
        sys.exit(1)

    prune(sys.argv[1])
