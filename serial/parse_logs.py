import re
import pandas as pd
import time

start = time.time()

log_file = "./data/access.log"

pattern = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<url>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<bytes>\S+)'
)

rows = []

with open(log_file, "r", errors="ignore") as file:
    for line in file:
        match = pattern.search(line)

        if match:
            rows.append(match.groupdict())

df = pd.DataFrame(rows)

end = time.time()

print(df.head())
print(f"Total Rows: {len(df)}")
print(f"Runtime: {end-start:.2f} seconds")