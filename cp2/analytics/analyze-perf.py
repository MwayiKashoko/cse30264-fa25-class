import sys
import os
import subprocess
import re
from collections import defaultdict
import statistics

def parse_pcap_file(pcap_file):
    try:
        # Get basic packet count
        cmd_count = ['tcpdump', '-r', pcap_file, '-n', 'tcp']
        #Had to use Stackoverflow to see how to run command line functions in Python
        result_count = subprocess.run(cmd_count, capture_output=True, text=True)
        total_packets = len([l for l in result_count.stdout.split('\n') if l.strip()])
        
        retrans_data = analyze_retransmissions_tcpdump(pcap_file)
        macs = extract_mac_addresses(pcap_file)
        
        return {
            'filename': os.path.basename(pcap_file),
            'total_packets': total_packets,
            'host_mac': macs.get('host'),
            'ap_mac': macs.get('ap'),
            'retransmissions': retrans_data
        }
    
    except Exception as e:
        print(f"Error parsing")
        return None

def analyze_retransmissions_tcpdump(pcap_file):
    try:
        cmd = ['tcpdump', '-r', pcap_file, '-n', '-v', 'tcp']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        flows = defaultdict(lambda: {
            'packets': [],
            'retrans_count': 0,
            'bytes': 0
        })
        
        lines = result.stdout.split('\n')
        
        for line in lines:
            if not line.strip():
                continue

            #I wish there was an easier way to do this but Regex is probably the fastest for both
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)\.(\d+) > (\d+\.\d+\.\d+\.\d+)\.(\d+)', line)
            if match:
                src_ip, src_port, dst_ip, dst_port = match.groups()
                flow_key = (src_ip, src_port, dst_ip, dst_port)
                
                seq_match = re.search(r'seq (\d+):?(\d+)?', line)
                if seq_match:
                    seq_start = int(seq_match.group(1))
                    seq_end = int(seq_match.group(2)) if seq_match.group(2) else seq_start
                    
                    if flows[flow_key]['packets']:
                        for prev_seq_start, prev_seq_end in flows[flow_key]['packets']:
                            if seq_start >= prev_seq_start and seq_start < prev_seq_end:
                                flows[flow_key]['retrans_count'] += 1
                                break
                    
                    flows[flow_key]['packets'].append((seq_start, seq_end))
                    flows[flow_key]['bytes'] += (seq_end - seq_start)
        
        data_flows = []
        for flow_key, flow_data in flows.items():
            if flow_data['bytes'] > 10000: #Arbitrary amount of bytes I decided for download data
                data_flows.append(flow_data['retrans_count'])
        
        return data_flows if data_flows else [0]
    
    except Exception as e:
        print(f"Error analyzing retransmissions")
        return [0]

def extract_mac_addresses(pcap_file):
    try:
        cmd = ['tcpdump', '-r', pcap_file, '-n', '-e', '-c', '100']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        macs = set()
        for line in result.stdout.split('\n'):
            # Look for MAC addresses in format: xx:xx:xx:xx:xx:xx, Not as bad as I thought it would be it's just repeated Regex for the most part
            mac_matches = re.findall(r'([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})', line.lower())
            macs.update(mac_matches)
        
        mac_list = list(macs)

        return {
            'host': mac_list[0] if len(mac_list) > 0 else 'unknown',
            'ap': mac_list[1] if len(mac_list) > 1 else 'unknown'
        }
    
    except Exception as e:
        print(f"Error extracting MAC addresses")
        return {'host': 'unknown', 'ap': 'unknown'}

def compute_statistics(values):
    if not values:
        return {'min': 0, 'max': 0, 'mean': 0, 'median': 0}
    
    return {
        'min': min(values),
        'max': max(values),
        'mean': statistics.mean(values),
        'median': statistics.median(values)
    }

def analyze_directory(directory):
    pcap_files = [f for f in os.listdir(directory) if f.endswith('.pcap')]
    
    if not pcap_files:
        print(f"No .pcap files found in {directory}")
        return
    
    print(f"Found {len(pcap_files)} .pcap files to analyze\n")
    print("=" * 80)
    
    all_captures = []
    node_data = defaultdict(lambda: {
        'host_mac': None,
        'ap_mac': None,
        'test_count': 0,
        'all_retrans': []
    })
    
    for pcap_file in sorted(pcap_files):
        filepath = os.path.join(directory, pcap_file)
        print(f"\nProcessing: {pcap_file}")
        
        capture_data = parse_pcap_file(filepath)
        if capture_data:
            all_captures.append(capture_data)
            
            host_mac = capture_data['host_mac']
            ap_mac = capture_data['ap_mac']
            node_key = (host_mac, ap_mac)
            
            node_data[node_key]['host_mac'] = host_mac
            node_data[node_key]['ap_mac'] = ap_mac
            node_data[node_key]['test_count'] += 1
            node_data[node_key]['all_retrans'].extend(capture_data['retransmissions'])
            
            stats = compute_statistics(capture_data['retransmissions'])
            print(f"  Total packets: {capture_data['total_packets']}")
            print(f"  Host MAC: {host_mac}")
            print(f"  AP MAC: {ap_mac}")
            print(f"  TCP Retransmissions - Min: {stats['min']}, Max: {stats['max']}, " +
                  f"Mean: {stats['mean']:.2f}, Median: {stats['median']:.2f}")
    
    print("\n" + "=" * 80)
    print("\nSUMMARY STATISTICS")
    print("=" * 80)
    
    print("\nTests per Host/AP Combination:")
    print("-" * 80)
    sorted_nodes = sorted(node_data.items(), key=lambda x: x[1]['test_count'], reverse=True)
    for (host, ap), data in sorted_nodes:
        print(f"  Host: {host}, AP: {ap} - {data['test_count']} tests")
    
    print("\n\nPerformance Analysis (sorted by mean retransmissions):")
    print("-" * 80)
    print(f"{'Host MAC':<20} {'AP MAC':<20} {'Tests':<8} {'Min':<6} {'Max':<6} {'Mean':<8} {'Median':<8}")
    print("-" * 80)
    
    sorted_by_perf = sorted(node_data.items(), 
                           key=lambda x: compute_statistics(x[1]['all_retrans'])['mean'], 
                           reverse=True)
    
    for (host, ap), data in sorted_by_perf:
        stats = compute_statistics(data['all_retrans'])
        print(f"{host:<20} {ap:<20} {data['test_count']:<8} " +
              f"{stats['min']:<6} {stats['max']:<6} {stats['mean']:<8.2f} {stats['median']:<8.2f}")
    
    print("\n" + "=" * 80)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)
    
    analyze_directory(directory)

if __name__ == "__main__":
    main()