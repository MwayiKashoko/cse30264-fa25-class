import os, sys, tarfile
from pto import prune


def packet_smash(input_dir, output_tar):
    tmp_files = []
    total_orig_size = 0
    num_captures = 0

    for file in os.listdir(input_dir):
        if file.endswith(".pcap"):
            full_path = os.path.join(input_dir, file)
            num_captures += 1
            total_orig_size += os.path.getsize(full_path)
            prune(full_path)
            tmp_files.append(f"pto-{file}")

    with tarfile.open(output_tar, "w:gz") as tar:
        for f in tmp_files:
            tar.add(f)

    final_size = os.path.getsize(output_tar)
    reduction = 100 * (total_orig_size - final_size) / total_orig_size if total_orig_size else 0

    print(f"Number of captures: {num_captures}")
    print(f"Cumulative size of original captures: {total_orig_size / 1024:.2f} KB")
    print(f"Final archive size: {final_size / 1024:.2f} KB")
    print(f"Percent reduction: {reduction:.2f}%")
    print(f"Smash complete: {output_tar}")

if len(sys.argv) < 3:
    print("Usage: python3 packet-smash.py <input_dir> <output_dir>")
    sys.exit(1)

input_dir = sys.argv[1]
output_dir = sys.argv[2]

output_tar = os.path.join(output_dir, "smash.tar.gz")
packet_smash(input_dir, output_tar)