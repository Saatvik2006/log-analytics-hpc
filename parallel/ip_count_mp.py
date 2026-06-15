import re
import os
import time
from multiprocessing import Pool

pattern = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<bytes>\S+)'
)


def count_ips(lines):

    print(
    f"PID {os.getpid()} processing {len(lines)} lines"
)

    ip_counts = {}

    for line in lines:

        match = pattern.search(line)

        if match:

            ip = match.group("ip")

            if ip not in ip_counts:
                ip_counts[ip] = 0

            ip_counts[ip] += 1

    return ip_counts


if __name__ == "__main__":

    start = time.time()

    with open("./data/access.log", "r", errors="ignore") as f:
        lines = f.readlines()

    num_workers = 4

    chunk_size = len(lines) // num_workers

    chunks = []

    for i in range(num_workers):

        start_idx = i * chunk_size

        if i == num_workers - 1:
            end_idx = len(lines)
        else:
            end_idx = (i + 1) * chunk_size

        chunks.append(lines[start_idx:end_idx])

    with Pool(num_workers) as pool:

        results = pool.map(count_ips, chunks)

    final_counts = {}

    for worker_result in results:

        for ip, count in worker_result.items():

            if ip not in final_counts:
                final_counts[ip] = 0

            final_counts[ip] += count

    end = time.time()

    print(f"Unique IPs: {len(final_counts)}")

    top_ips = sorted(
        final_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    print("\nTop 10 IPs:")

    for ip, count in top_ips:
        print(ip, count)

    print(f"\nRuntime: {end-start:.2f} seconds")