import re
import os

from mpi4py import MPI

LOG_FILE = "../data/access.log"

pattern = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<bytes>\S+)'
)

comm = MPI.COMM_WORLD

rank = comm.Get_rank()
size = comm.Get_size()

# ------------------------------------
# Rank 0 computes file partitions
# ------------------------------------

if rank == 0:

    file_size = os.path.getsize(LOG_FILE)

    chunk_size = file_size // size

    partitions = []

    for i in range(size):

        start_byte = i * chunk_size

        if i == size - 1:
            end_byte = file_size
        else:
            end_byte = (i + 1) * chunk_size

        partitions.append(
            (start_byte, end_byte)
        )

else:

    partitions = None

# ------------------------------------
# Scatter work
# ------------------------------------

partition = comm.scatter(
    partitions,
    root=0
)

start_byte, end_byte = partition

# ------------------------------------
# Start benchmark
# ------------------------------------

comm.Barrier()

start_time = MPI.Wtime()

# ------------------------------------
# Local counting
# ------------------------------------

ip_counts = {}

with open(LOG_FILE, "r", errors="ignore") as f:

    f.seek(start_byte)

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

# ------------------------------------
# Gather results
# ------------------------------------

results = comm.gather(
    ip_counts,
    root=0
)

# ------------------------------------
# Synchronize before stopping timer
# ------------------------------------

comm.Barrier()

end_time = MPI.Wtime()

# ------------------------------------
# Merge on Rank 0
# ------------------------------------

if rank == 0:

    final_counts = {}

    for worker_result in results:

        for ip, count in worker_result.items():

            if ip not in final_counts:
                final_counts[ip] = 0

            final_counts[ip] += count

    top_ips = sorted(
        final_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    print(f"Unique IPs: {len(final_counts)}")

    print("\nTop 10 IPs:")

    for ip, count in top_ips:
        print(ip, count)

    print(
        f"\nRuntime: {end_time - start_time:.2f} s"
    )