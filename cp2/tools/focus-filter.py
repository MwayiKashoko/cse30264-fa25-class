import sys
import pyshark
import subprocess

def focus_filter(pcap_file, output_file):
    cap = pyshark.FileCapture(pcap_file, keep_packets=False)
    #Had to use Stackoverflow to see how to run command line functions in Python
    client_ip = subprocess.run(
        ['python3', 'find-client.py', pcap_file],
        capture_output=True, text=True
    ).stdout.strip()

    server_ip = subprocess.run(
        ['python3', 'find-server.py', pcap_file],
        capture_output=True, text=True
    ).stdout.strip()

    #cap = pyshark.FileCapture(pcap_file, output_file=output_file, display_filter=f"(ip.src=={client_ip} and ip.dst=={server_ip}) or (ip.src=={server_ip} and ip.dst=={client_ip})", keep_packets=False)
    #cap.load_packets()

    #Runs WAY TOO SLOWLY if I don't use tshark
    #-r reads file, -w writes to file, -Y allows for display filter
    #Also used Stackoverflow to figure out how to use tshark since pyshar.FileCapture was running slowly and taking up ~10gb of memory
    cmd = [
        "tshark",
        "-r", pcap_file,
        "-Y", f"(ip.src=={client_ip} && ip.dst=={server_ip}) || (ip.src=={server_ip} && ip.dst=={client_ip})",
        "-w", output_file
    ]

    subprocess.run(cmd)

if __name__ == "__main__":
    focus_filter(sys.argv[1], sys.argv[2])