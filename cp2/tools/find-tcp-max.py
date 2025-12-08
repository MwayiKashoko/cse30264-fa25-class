import sys
import subprocess

def find_tcp_max(pcap_file):
    #-r reads file, -Y allows for display filter, -T output format, -e fields to include in output, vlan.id is necessary apparently get 0 if I don't have that there
    #Also used Stackoverflow to figure out how to use tshark since pyshar.FileCapture was running slowly and taking up ~10gb of memory
    cmd = [
        "tshark", "-r", pcap_file,
        "-Y", "tcp",
        "-T", "fields",
        "-e", "frame.encap_type",
        "-e", "ip.hdr_len",
        "-e", "tcp.hdr_len",
        "-e", "vlan.id"
    ]

    #Had to use Stackoverflow to see how to run command line functions in Python
    result = subprocess.run(cmd, capture_output=True, text=True)
    max_len = 0

    for line in result.stdout.splitlines():
        fields = line.split("\t")
        if len(fields) != 4:
            continue

        encap, ip_hdr, tcp_hdr, vlan = fields

        if encap == "1": #Ethernet header
            l2 = 14 + (4 if vlan else 0) #Ethernet headers are 14 bytes and have to add 4 if vlan exists to account for full size
        else:
            continue

        try:
            ip_hdr = int(ip_hdr)
            tcp_hdr = int(tcp_hdr)
        except:
            continue

        header_len = l2 + ip_hdr + tcp_hdr
        
        if header_len > max_len:
            max_len = header_len

    return max_len


if __name__ == "__main__":
    print(find_tcp_max(sys.argv[1]))
