#!/usr/bin/env python3
"""
GPU Acceleration Benchmark for GCT Assistant on M4 Max
Tests GPU acceleration performance across different operations
"""

import requests
import time
import numpy as np
import json
from datetime import datetime

BASE_URL = "http://localhost:5001"

def generate_test_profiles(count):
    """Generate test profile data"""
    profiles = []
    for i in range(count):
        profiles.append({
            'user_id': f'test_user_{i}',
            'variables': {
                'psi': np.random.uniform(0.3, 0.9),
                'rho': np.random.uniform(0.3, 0.9),
                'q': np.random.uniform(0.3, 0.9),
                'f': np.random.uniform(0.3, 0.9)
            },
            'tier': 1
        })
    return profiles

def test_batch_coherence():
    """Test GPU-accelerated batch coherence calculation"""
    print("\n🚀 Testing Batch Coherence Calculation")
    print("=" * 50)
    
    test_sizes = [10, 50, 100, 500, 1000, 5000]
    
    for size in test_sizes:
        profiles = generate_test_profiles(size)
        
        # Test GPU acceleration
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/gpu/batch_coherence",
            json={'profiles': profiles, 'operation': 'static_coherence'}
        )
        gpu_time = (time.time() - start) * 1000
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nBatch size: {size}")
            print(f"  Total time: {gpu_time:.2f}ms")
            print(f"  GPU time: {data['performance']['gpu_time_ms']:.2f}ms")
            print(f"  Speedup: {data['performance']['speedup_factor']}")
            print(f"  Throughput: {int(size / (gpu_time / 1000)):,} profiles/sec")
        else:
            print(f"Error for size {size}: {response.status_code}")

def test_similarity_analysis():
    """Test GPU-accelerated similarity analysis"""
    print("\n🚀 Testing Similarity Analysis")
    print("=" * 50)
    
    # First, create some test profiles
    profiles = generate_test_profiles(100)
    user_ids = []
    
    # Store profiles in database
    for profile in profiles[:50]:  # Use first 50
        response = requests.post(
            f"{BASE_URL}/api/assessment/tier1",
            json={
                'user_id': profile['user_id'],
                'responses': {
                    'consistency': profile['variables']['psi'],
                    'wisdom': profile['variables']['rho'],
                    'energy': profile['variables']['q'],
                    'belonging': profile['variables']['f']
                },
                'age': 30
            }
        )
        if response.status_code == 200:
            user_ids.append(profile['user_id'])
    
    # Test similarity computation
    if user_ids:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/gpu/similarity_analysis",
            json={'user_ids': user_ids, 'metric': 'euclidean'}
        )
        total_time = (time.time() - start) * 1000
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nProfiles analyzed: {data['profiles_analyzed']}")
            print(f"Total time: {total_time:.2f}ms")
            print(f"GPU speedup: {data['performance']['speedup_factor']}")
            print(f"Most similar pairs:")
            for pair in data['most_similar_pairs'][:3]:
                print(f"  {pair['user1']} <-> {pair['user2']}: {pair['similarity']:.3f}")

def test_pattern_matching():
    """Test GPU-accelerated pattern matching"""
    print("\n🚀 Testing Pattern Matching")
    print("=" * 50)
    
    # Use existing user IDs from previous test
    user_ids = [f'test_user_{i}' for i in range(20)]
    
    start = time.time()
    response = requests.post(
        f"{BASE_URL}/api/gpu/pattern_matching",
        json={'user_ids': user_ids}
    )
    total_time = (time.time() - start) * 1000
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nProfiles analyzed: {data['profiles_analyzed']}")
        print(f"Total time: {total_time:.2f}ms")
        print(f"GPU speedup: {data['performance']['speedup_factor']}")
        print(f"\nArchetype Distribution:")
        
        archetype_counts = {}
        for user in data['user_archetypes']:
            arch = user['archetype']
            archetype_counts[arch] = archetype_counts.get(arch, 0) + 1
        
        for arch, count in archetype_counts.items():
            print(f"  {arch}: {count} users")

def test_gpu_benchmark():
    """Run comprehensive GPU benchmark"""
    print("\n🚀 Running GPU Benchmark")
    print("=" * 50)
    
    response = requests.post(
        f"{BASE_URL}/api/gpu/benchmark",
        json={'test_sizes': [10, 100, 1000, 5000, 10000]}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nGPU Enabled: {data['gpu_enabled']}")
        print(f"Device: {data['device_info']['name']}")
        print(f"GPU Cores: {data['device_info']['gpu_cores']}")
        print(f"Neural Engine: {data['device_info']['neural_engine']}")
        
        print("\nBenchmark Results:")
        print(f"{'Batch Size':>12} {'Time (ms)':>12} {'Per Item (μs)':>15} {'Speedup':>10} {'Throughput/s':>15}")
        print("-" * 75)
        
        for result in data['benchmark_results']:
            print(f"{result['batch_size']:>12} "
                  f"{result['total_time_ms']:>12.2f} "
                  f"{result['per_item_us']:>15.2f} "
                  f"{result['speedup']:>10} "
                  f"{result['throughput_per_second']:>15,}")

def test_group_optimization():
    """Test GPU-accelerated group optimization"""
    print("\n🚀 Testing Group Optimization")
    print("=" * 50)
    
    # Use a subset of users for optimization
    user_ids = [f'test_user_{i}' for i in range(20)]
    
    start = time.time()
    response = requests.post(
        f"{BASE_URL}/api/gpu/group_optimization",
        json={
            'user_ids': user_ids,
            'target_coherence': 3.0,
            'max_iterations': 50
        }
    )
    total_time = (time.time() - start) * 1000
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nGroup size: {data['group_size']}")
        print(f"Current average coherence: {data['current_average_coherence']:.3f}")
        print(f"Target coherence: {data['target_coherence']}")
        print(f"Predicted average coherence: {data['predicted_average_coherence']:.3f}")
        print(f"Improvement: {data['improvement_percentage']:.1f}%")
        print(f"\nPerformance:")
        print(f"  Total time: {total_time:.2f}ms")
        print(f"  GPU speedup: {data['performance']['speedup_factor']}")

def main():
    print("🚀 M4 Max GPU Acceleration Benchmark for GCT Assistant")
    print("=" * 60)
    print(f"Timestamp: {datetime.now()}")
    print(f"Backend URL: {BASE_URL}")
    
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
    
    # Run all tests
    test_batch_coherence()
    test_similarity_analysis()
    test_pattern_matching()
    test_group_optimization()
    test_gpu_benchmark()
    
    # Get performance summary
    print("\n📊 Overall GPU Performance Summary")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/api/gpu/performance_stats")
    if response.status_code == 200:
        data = response.json()
        print(f"Total operations: {data['total_operations']}")
        print(f"Average speedup: {data['average_speedup']}")
        print(f"Total items processed: {data['total_items_processed']:,}")
        print(f"GPU time saved: {data['gpu_time_saved_ms']}ms")
        
        if data['operation_breakdown']:
            print("\nRecent operations:")
            for op in data['operation_breakdown']:
                print(f"  {op['operation']}: {op['speedup']} speedup, {op['items']} items")
    
    print("\n✅ GPU Benchmark complete!")
    print("\n💡 Recommendations:")
    print("- Use batch operations for maximum GPU utilization")
    print("- Batch sizes > 100 show significant speedup")
    print("- Consider GPU acceleration for real-time group analysis")
    print("- Neural Engine can be leveraged for pattern recognition tasks")

if __name__ == "__main__":
    main()