import re
import pandas as pd
import time
from multiprocessing import Pool

pattern = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<bytes>\S+)'
)

def parse_chunk(lines):

    rows = []

    for line in lines:

        match = pattern.search(line)

        if match:
            rows.append(match.groupdict())

    return rows


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

        results = pool.map(parse_chunk, chunks)

    rows = []

    for chunk_result in results:
        rows.extend(chunk_result)

    df = pd.DataFrame(rows)

    end = time.time()

    print(f"Rows Parsed: {len(df)}")
    print(f"Runtime: {end-start:.2f} seconds")