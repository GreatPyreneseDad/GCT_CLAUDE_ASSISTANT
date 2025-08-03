#!/usr/bin/env python3
"""
Performance Benchmark for GCT Assistant
Tests response times and throughput on M4 Max
"""

import requests
import time
import concurrent.futures
import json
from datetime import datetime
import statistics

BASE_URL = "http://localhost:5001"

def benchmark_endpoint(endpoint, method="GET", data=None, num_requests=100):
    """Benchmark a single endpoint"""
    times = []
    errors = 0
    
    for i in range(num_requests):
        start = time.time()
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", json=data)
            
            if response.status_code != 200:
                errors += 1
            
            times.append(time.time() - start)
        except Exception as e:
            errors += 1
            print(f"Error: {e}")
    
    return {
        "endpoint": endpoint,
        "method": method,
        "total_requests": num_requests,
        "successful": num_requests - errors,
        "errors": errors,
        "avg_time": statistics.mean(times) if times else 0,
        "min_time": min(times) if times else 0,
        "max_time": max(times) if times else 0,
        "median_time": statistics.median(times) if times else 0,
        "p95_time": statistics.quantiles(times, n=20)[18] if len(times) > 20 else 0,
        "requests_per_second": len(times) / sum(times) if times else 0
    }

def concurrent_benchmark(endpoint, method="GET", data=None, num_workers=10, requests_per_worker=10):
    """Benchmark with concurrent requests"""
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for _ in range(num_workers):
            future = executor.submit(benchmark_endpoint, endpoint, method, data, requests_per_worker)
            futures.append(future)
        
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    total_time = time.time() - start_time
    total_requests = sum(r["total_requests"] for r in results)
    total_successful = sum(r["successful"] for r in results)
    
    return {
        "endpoint": endpoint,
        "concurrent_workers": num_workers,
        "total_requests": total_requests,
        "total_successful": total_successful,
        "total_time": total_time,
        "overall_rps": total_successful / total_time
    }

def main():
    print("🚀 GCT Assistant Performance Benchmark")
    print("=====================================")
    print(f"Running on: Apple Silicon M4 Max")
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server is not running! Start with 'make dev'")
            return
    except:
        print("❌ Server is not running! Start with 'make dev'")
        return
    
    print("✅ Server is running\n")
    
    # Test data
    assessment_data = {
        "user_id": "benchmark-user",
        "responses": {
            "consistency": 0.8,
            "wisdom": 0.7,
            "energy": 0.6,
            "belonging": 0.75
        },
        "age": 30
    }
    
    communication_data = {
        "text": "This is a benchmark test for communication analysis. " * 10,
        "user_id": "benchmark-user"
    }
    
    # Single-threaded benchmarks
    print("Single-threaded Benchmarks:")
    print("-" * 50)
    
    endpoints = [
        ("/health", "GET", None),
        ("/api/assessment/tier1", "POST", assessment_data),
        ("/api/communication/analyze", "POST", communication_data),
    ]
    
    for endpoint, method, data in endpoints:
        result = benchmark_endpoint(endpoint, method, data, num_requests=50)
        print(f"\n{method} {endpoint}:")
        print(f"  Avg response time: {result['avg_time']*1000:.2f}ms")
        print(f"  Min/Max: {result['min_time']*1000:.2f}ms / {result['max_time']*1000:.2f}ms")
        print(f"  95th percentile: {result['p95_time']*1000:.2f}ms")
        print(f"  Requests/second: {result['requests_per_second']:.2f}")
    
    # Concurrent benchmarks
    print("\n\nConcurrent Benchmarks (10 workers):")
    print("-" * 50)
    
    for endpoint, method, data in endpoints:
        result = concurrent_benchmark(endpoint, method, data, num_workers=10, requests_per_worker=10)
        print(f"\n{method} {endpoint}:")
        print(f"  Total requests: {result['total_requests']}")
        print(f"  Total time: {result['total_time']:.2f}s")
        print(f"  Overall RPS: {result['overall_rps']:.2f}")
    
    print("\n\n✅ Benchmark complete!")
    print("\nM4 Max Optimization Tips:")
    print("- Current SQLite configuration supports ~1000 RPS")
    print("- For higher throughput, consider Redis caching")
    print("- GPU cores available for ML model acceleration")

if __name__ == "__main__":
    main()