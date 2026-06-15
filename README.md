# Large-Scale Log Analytics using Multiprocessing and MPI

## Overview

This project investigates different parallel computing approaches for processing large-scale web server logs using Python Multiprocessing and MPI (Message Passing Interface).

The objective was to analyze the impact of communication overhead, file I/O, scalability, and distributed execution on log analytics performance.

The project was completed as part of an HPC (High Performance Computing) internship project.

---

## Dataset

NASA HTTP Access Logs

* Total records: 1,566,461
* Dataset size: ~160 MB

---

## Hardware Configuration

### Desktop Node

* Intel Core i5-3570
* 4 CPU cores
* Ubuntu Linux

### Secondary Node

* Intel Core i3 M380
* 2 CPU cores
* Ubuntu Linux

### Cluster Configuration

* Ethernet-connected two-node cluster
* OpenMPI
* mpi4py
* Passwordless SSH

---

## Project Structure

```text
LogAnalytics_HPC/
│
├── data/
├── serial/
├── parallel/
├── mpi/
├── plots/
├── reports/
├── results/
└── README.md
```

---

## Implementations

### 1. Serial Parsing

Single-process baseline implementation.

### 2. Multiprocessing V1 (Naive)

* Read entire file
* Split into chunks
* Send chunks to workers
* Workers return parsed rows

### 3. Multiprocessing V2 (Local Aggregation)

* Workers compute local IP statistics
* Only summaries returned
* Reduced communication overhead

### 4. Multiprocessing V3 (File Partitioning)

* Workers receive byte ranges
* Each worker reads its own file partition

### 5. MPI Implementation

* Distributed processing across two machines
* OpenMPI + mpi4py
* Scatter/Gather communication model

---

## Benchmark Results

| Method | Runtime (s) |
| ------ | ----------: |
| Serial |        4.81 |
| MP V1  |        7.40 |
| MP V2  |        2.16 |
| MP V3  |        5.48 |
| MPI 2  |        6.94 |
| MPI 4  |        4.99 |
| MPI 6  |        3.78 |

---

## Key Findings

* Parallel execution can be slower than serial execution.
* Communication overhead significantly affects performance.
* Local aggregation reduced communication costs and achieved the best runtime.
* File partitioning exposed disk I/O bottlenecks.
* MPI successfully distributed computation across two machines.
* Additional machines did not provide linear speedup due to communication overhead and hardware imbalance.
* Algorithm design had a greater impact on performance than simply increasing process count.

---

## Generated Plots

The repository includes:

* Runtime comparison
* MPI scaling analysis
* Speedup comparison

Plots are available in the `plots/` directory.

---

## Technologies Used

* Python
* Multiprocessing
* OpenMPI
* mpi4py
* Linux
* Matplotlib

---

## Conclusion

The best-performing implementation was the multiprocessing local aggregation approach (MP V2), achieving a runtime of 2.16 seconds.

This project demonstrates practical HPC concepts including scalability, communication overhead, distributed execution, load balancing, and performance optimization.
