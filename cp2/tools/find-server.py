import sys
import pyshark

def find_server(pcap_file):
    cap = pyshark.FileCapture(pcap_file, keep_packets=False)

    for pkt in cap:
        if hasattr(pkt, 'tcp'):
            #Is ACK flag set
            tcp_flags = int(pkt.tcp.flags, 16)
            #Is SYN flag set
            syn_flag = 2
           
            #Check if both flags are set
            if tcp_flags & syn_flag and not tcp_flags & 16:
                print(pkt.ip.dst)
                cap.close()
                return

if __name__ == "__main__":
    find_server(sys.argv[1])
