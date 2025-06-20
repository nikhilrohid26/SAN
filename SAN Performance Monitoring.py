# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14suMf1Kgxmv6S7QSuQtXnJ_c4ejD-taV
"""

import random
import time
import csv
from datetime import datetime

# Simulate SAN disk operations
class SANPerformanceMonitor:
    def __init__(self, disk_size_gb=100):
        self.disk_size_gb = disk_size_gb
        self.operations = []

    def simulate_io_operations(self, num_operations=1000):
        for _ in range(num_operations):
            op_type = random.choice(["read", "write"])
            block_size_kb = random.randint(4, 64)  # Random block size (4KB-64KB)
            latency_ms = random.uniform(0.1, 5.0)  # Simulate latency (0.1ms - 5ms)

            # Record operation
            self.operations.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operation": op_type,
                "block_size_kb": block_size_kb,
                "latency_ms": latency_ms
            })
            time.sleep(0.001)  # Small delay

    def calculate_metrics(self):
        total_reads = sum(1 for op in self.operations if op["operation"] == "read")
        total_writes = len(self.operations) - total_reads

        avg_latency = sum(op["latency_ms"] for op in self.operations) / len(self.operations)
        total_throughput_mb = sum(op["block_size_kb"] for op in self.operations) / 1024  # Convert to MB

        return {
            "total_operations": len(self.operations),
            "read_operations": total_reads,
            "write_operations": total_writes,
            "avg_latency_ms": round(avg_latency, 2),
            "total_throughput_mb": round(total_throughput_mb, 2),
            "iops": len(self.operations)  # IOPS = Total operations per second (simplified)
        }

    def save_to_csv(self, filename="san_performance_log.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.operations[0].keys())
            writer.writeheader()
            writer.writerows(self.operations)
        print(f"Performance log saved to {filename}")

# Run simulation
if __name__ == "__main__":
    san_monitor = SANPerformanceMonitor()
    print("Simulating SAN I/O operations...")
    san_monitor.simulate_io_operations(num_operations=500)

    metrics = san_monitor.calculate_metrics()
    print("\n=== SAN Performance Metrics ===")
    print(f"Total Operations: {metrics['total_operations']}")
    print(f"Read Operations: {metrics['read_operations']}")
    print(f"Write Operations: {metrics['write_operations']}")
    print(f"Avg Latency: {metrics['avg_latency_ms']} ms")
    print(f"Total Throughput: {metrics['total_throughput_mb']} MB")
    print(f"IOPS: {metrics['iops']}")

    san_monitor.save_to_csv()

import matplotlib.pyplot as plt

def plot_metrics(operations):
    latencies = [op["latency_ms"] for op in operations]
    plt.hist(latencies, bins=20, edgecolor="black")
    plt.title("SAN Operation Latency Distribution")
    plt.xlabel("Latency (ms)")
    plt.ylabel("Frequency")
    plt.show()

def check_for_latency_spikes(operations, threshold_ms=4.0):
    spikes = [op for op in operations if op["latency_ms"] > threshold_ms]
    print(f"⚠️ Found {len(spikes)} operations exceeding {threshold_ms}ms latency!")

plot_metrics(san_monitor.operations)

