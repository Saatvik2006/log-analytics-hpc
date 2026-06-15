import matplotlib.pyplot as plt

# -------------------------
# Benchmark Results
# -------------------------

methods = [
    "Serial",
    "MP V1",
    "MP V2",
    "MP V3",
    "MPI 2",
    "MPI 4",
    "MPI 6"
]

runtimes = [
    4.81,
    7.40,
    2.16,
    5.48,
    6.94,
    4.99,
    3.78
]

# -------------------------
# Plot 1
# Runtime Comparison
# -------------------------

plt.figure(figsize=(10, 6))

plt.bar(methods, runtimes)

plt.ylabel("Runtime (seconds)")
plt.xlabel("Implementation")
plt.title("Log Analytics Runtime Comparison")

plt.tight_layout()

plt.savefig("runtime_comparison.png")

plt.close()

# -------------------------
# Plot 2
# MPI Scaling
# -------------------------

ranks = [2, 4, 6]

mpi_runtimes = [
    6.94,
    4.99,
    3.78
]

plt.figure(figsize=(8, 5))

plt.plot(
    ranks,
    mpi_runtimes,
    marker="o"
)

plt.xlabel("MPI Ranks")
plt.ylabel("Runtime (seconds)")
plt.title("MPI Scaling Performance")

plt.grid(True)

plt.tight_layout()

plt.savefig("mpi_scaling.png")

plt.close()

print("Plots generated successfully.")

# -------------------------
# Plot 3
# Speedup
# -------------------------

serial_time = 4.81

speedups = [
    serial_time / 7.40,
    serial_time / 2.16,
    serial_time / 5.48,
    serial_time / 6.94,
    serial_time / 4.99,
    serial_time / 3.78
]

labels = [
    "MP V1",
    "MP V2",
    "MP V3",
    "MPI 2",
    "MPI 4",
    "MPI 6"
]

plt.figure(figsize=(10, 6))

plt.bar(labels, speedups)

plt.ylabel("Speedup")
plt.xlabel("Implementation")
plt.title("Speedup Relative to Serial Execution")

plt.tight_layout()

plt.savefig("speedup_comparison.png")

plt.close()