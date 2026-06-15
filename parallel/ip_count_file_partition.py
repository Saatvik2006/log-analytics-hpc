import re
import time
import os
from multiprocessing import Pool

LOG_FILE = "./data/access.log"

pattern = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<bytes>\S+)'
)


def count_ips_partition(args):

    start_byte, end_byte = args

    ip_counts = {}

    with open(LOG_FILE, "r", errors="ignore") as f:

        f.seek(start_byte)

        # Boundary fix
        if start_byte != 0:
            f.readline()

        while f.tell() < end_byte:

            line = f.readline()

            if not line:
                break

            match = pattern.search(line)

            if match:

                ip = match.group("ip")

                if ip not in ip_counts:
                    ip_counts[ip] = 0

                ip_counts[ip] += 1

    print(
        f"PID {os.getpid()} processed "
        f"{sum(ip_counts.values())} lines"
    )

    return ip_counts


if __name__ == "__main__":

    start = time.time()

    file_size = os.path.getsize(LOG_FILE)

    num_workers = 4

    chunk_size = file_size // num_workers

    partitions = []

    for i in range(num_workers):

        start_byte = i * chunk_size

        if i == num_workers - 1:
            end_byte = file_size
        else:
            end_byte = (i + 1) * chunk_size

        partitions.append(
            (start_byte, end_byte)
        )

    with Pool(num_workers) as pool:

        results = pool.map(
            count_ips_partition,
            partitions
        )

    final_counts = {}

    for worker_result in results:

        for ip, count in worker_result.items():

            if ip not in final_counts:
                final_counts[ip] = 0

            final_counts[ip] += count

    end = time.time()

    print(f"\nUnique IPs: {len(final_counts)}")

    top_ips = sorted(
        final_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    print("\nTop 10 IPs:")

    for ip, count in top_ips:
        print(ip, count)

    print(f"\nRuntime: {end-start:.2f} seconds")