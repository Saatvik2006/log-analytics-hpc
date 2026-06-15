# Large-Scale Log Analytics using Multiprocessing and MPI

## Overview

This project investigates the performance of multiple parallel computing approaches for large-scale log analytics using the NASA HTTP access log dataset containing approximately 1.56 million records.

The objective was to study how different parallelization strategies affect execution time and scalability while processing large log files.

## System Configuration

### Desktop Node

* Intel Core i5-3570
* 4 CPU cores
* Ubuntu Linux

### Secondary Node

* Intel Core i3 M380
* 2 CPU cores
* Ubuntu Linux

### Cluster Configuration

* Ethernet-connected two-node MPI cluster
* OpenMPI
* mpi4py

---

## Implementations

### Serial Parser

Single-process baseline implementation.

Runtime:

4.81 seconds

### Multiprocessing V1 (Naive)

Workflow:

Read file → split data → send chunks to workers → parse → return parsed rows.

Runtime:

7.40 seconds

Observation:

Communication overhead exceeded computation benefit.

### Multiprocessing V2 (Local Aggregation)

Workers computed local IP statistics and returned only summaries.

Runtime:

2.16 seconds

Observation:

Reducing communication significantly improved performance.

### Multiprocessing V3 (File Partitioning)

Workers independently read byte ranges of the file.

Runtime:

5.48 seconds

Observation:

Communication overhead decreased, but disk I/O became the dominant bottleneck.

### MPI Implementation

Distributed file partitioning across multiple MPI ranks.

Results:

* MPI 2 ranks: 6.94 s
* MPI 4 ranks: 4.99 s
* MPI 6 ranks (2-node cluster): 3.78 s

Observation:

Additional ranks improved performance, but speedup was limited by startup overhead, file I/O, communication costs, and load imbalance caused by heterogeneous hardware.

---

## Key HPC Lessons

1. Parallel execution can be slower than serial execution.
2. Communication overhead strongly impacts performance.
3. Local aggregation is often more important than increasing process count.
4. Reducing communication can expose I/O bottlenecks.
5. Distributed computing does not guarantee linear speedup.
6. Heterogeneous clusters introduce load imbalance.

---

## Conclusion

The most effective implementation was the local aggregation multiprocessing design, which achieved a runtime of 2.16 seconds.

Although MPI successfully distributed computation across two machines, the workload size and communication overhead prevented it from outperforming the optimized multiprocessing approach.

The project demonstrates practical HPC concepts including parallel speedup, communication overhead, scalability limits, load balancing, and distributed execution using MPI.
