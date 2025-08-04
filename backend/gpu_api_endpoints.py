# GPU-Accelerated API Endpoints
# High-performance endpoints leveraging M4 Max GPU acceleration

from flask import Blueprint, request, jsonify
import numpy as np
from typing import List, Dict
from datetime import datetime
import time
import sqlite3
import logging

# Import GPU acceleration
from gpu_acceleration import get_accelerator
from gct_types import CoherenceProfile, CoherenceVariables

# Set up logger
logger = logging.getLogger(__name__)

# Create blueprint
gpu_api = Blueprint('gpu_api', __name__)

# Get accelerator instance
accelerator = get_accelerator()

@gpu_api.route('/gpu/batch_coherence', methods=['POST'])
def batch_coherence_calculation():
    """
    GPU-accelerated batch coherence calculation
    Processes multiple profiles in parallel on GPU
    """
    try:
        data = request.json
        profile_data = data.get('profiles', [])
        operation = data.get('operation', 'static_coherence')
        
        if not profile_data:
            return jsonify({'error': 'No profiles provided'}), 400
        
        # Convert to CoherenceProfile objects
        profiles = []
        for p in profile_data:
            variables = CoherenceVariables(
                psi=p['variables']['psi'],
                rho=p['variables']['rho'],
                q=p['variables']['q'],
                f=p['variables']['f']
            )
            
            profile = CoherenceProfile(
                user_id=p.get('user_id', 'batch_user'),
                variables=variables,
                static_coherence=0,  # Will be calculated
                coherence_velocity=0,
                assessment_tier=p.get('tier', 1),
                timestamp=datetime.now()
            )
            profiles.append(profile)
        
        # GPU-accelerated calculation
        results, stats = accelerator.accelerate_coherence_batch(profiles, operation)
        
        # Format response
        response = {
            'batch_size': len(profiles),
            'operation': operation,
            'results': results,
            'performance': {
                'gpu_time_ms': stats.gpu_time_ms,
                'speedup_factor': f"{stats.speedup_factor:.2f}x",
                'gpu_enabled': accelerator.gpu_available
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Batch coherence error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@gpu_api.route('/gpu/similarity_analysis', methods=['POST'])
def similarity_analysis():
    """
    GPU-accelerated similarity analysis for profile clustering
    """
    try:
        data = request.json
        user_ids = data.get('user_ids', [])
        metric = data.get('metric', 'euclidean')
        
        if not user_ids:
            return jsonify({'error': 'No user IDs provided'}), 400
        
        # Fetch profiles from database
        profiles = []
        db = sqlite3.connect('gct_database.db')
        cursor = db.cursor()
        
        for user_id in user_ids:
            cursor.execute('''
                SELECT user_id, psi, rho, q, f, static_coherence, assessment_tier, timestamp
                FROM coherence_profiles
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                variables = CoherenceVariables(psi=row[1], rho=row[2], q=row[3], f=row[4])
                profile = CoherenceProfile(
                    user_id=row[0],
                    variables=variables,
                    static_coherence=row[5],
                    coherence_velocity=0,
                    assessment_tier=row[6],
                    timestamp=datetime.fromisoformat(row[7])
                )
                profiles.append(profile)
        
        db.close()
        
        if len(profiles) < 2:
            return jsonify({'error': 'Need at least 2 profiles for similarity analysis'}), 400
        
        # GPU-accelerated similarity computation
        similarity_matrix, stats = accelerator.accelerate_similarity_matrix(profiles, metric)
        
        # Find most similar pairs
        n = len(profiles)
        similar_pairs = []
        
        for i in range(n):
            for j in range(i + 1, n):
                similar_pairs.append({
                    'user1': profiles[i].user_id,
                    'user2': profiles[j].user_id,
                    'similarity': float(1 - similarity_matrix[i, j])  # Convert distance to similarity
                })
        
        # Sort by similarity
        similar_pairs.sort(key=lambda x: x['similarity'], reverse=True)
        
        response = {
            'profiles_analyzed': len(profiles),
            'metric': metric,
            'most_similar_pairs': similar_pairs[:10],  # Top 10
            'similarity_matrix_shape': similarity_matrix.shape,
            'performance': {
                'gpu_time_ms': stats.gpu_time_ms,
                'speedup_factor': f"{stats.speedup_factor:.2f}x",
                'items_processed': stats.items_processed
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Similarity analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@gpu_api.route('/gpu/pattern_matching', methods=['POST'])
def pattern_matching():
    """
    GPU-accelerated pattern matching for archetype identification
    """
    try:
        data = request.json
        user_ids = data.get('user_ids', [])
        
        # Define archetype patterns
        patterns = {
            'high_coherence': np.array([0.8, 0.8, 0.8, 0.8]),
            'wisdom_seeker': np.array([0.6, 0.9, 0.5, 0.6]),
            'action_oriented': np.array([0.7, 0.5, 0.9, 0.6]),
            'community_builder': np.array([0.6, 0.6, 0.6, 0.9]),
            'balanced': np.array([0.7, 0.7, 0.7, 0.7])
        }
        
        # Fetch profiles
        profiles = []
        db = sqlite3.connect('gct_database.db')
        cursor = db.cursor()
        
        for user_id in user_ids:
            cursor.execute('''
                SELECT user_id, psi, rho, q, f, static_coherence, assessment_tier, timestamp
                FROM coherence_profiles
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                variables = CoherenceVariables(psi=row[1], rho=row[2], q=row[3], f=row[4])
                profile = CoherenceProfile(
                    user_id=row[0],
                    variables=variables,
                    static_coherence=row[5],
                    coherence_velocity=0,
                    assessment_tier=row[6],
                    timestamp=datetime.fromisoformat(row[7])
                )
                profiles.append(profile)
        
        db.close()
        
        if not profiles:
            return jsonify({'error': 'No valid profiles found'}), 404
        
        # GPU-accelerated pattern matching
        matches, stats = accelerator.accelerate_pattern_matching(profiles, patterns)
        
        # Find best archetype for each user
        user_archetypes = []
        for i, profile in enumerate(profiles):
            best_match = None
            best_score = -1
            
            for pattern_name, scores in matches.items():
                if scores[i] > best_score:
                    best_score = scores[i]
                    best_match = pattern_name
            
            user_archetypes.append({
                'user_id': profile.user_id,
                'archetype': best_match,
                'confidence': float(best_score),
                'all_scores': {name: float(scores[i]) for name, scores in matches.items()}
            })
        
        response = {
            'profiles_analyzed': len(profiles),
            'archetypes': list(patterns.keys()),
            'user_archetypes': user_archetypes,
            'performance': {
                'gpu_time_ms': stats.gpu_time_ms,
                'speedup_factor': f"{stats.speedup_factor:.2f}x",
                'patterns_tested': len(patterns)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Pattern matching error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@gpu_api.route('/gpu/group_optimization', methods=['POST'])
def group_optimization():
    """
    GPU-accelerated group coherence optimization
    """
    try:
        data = request.json
        user_ids = data.get('user_ids', [])
        target_coherence = data.get('target_coherence', 3.0)
        max_iterations = data.get('max_iterations', 50)
        
        if not user_ids:
            return jsonify({'error': 'No user IDs provided'}), 400
        
        # Fetch profiles
        profiles = []
        db = sqlite3.connect('gct_database.db')
        cursor = db.cursor()
        
        for user_id in user_ids:
            cursor.execute('''
                SELECT user_id, psi, rho, q, f, static_coherence, assessment_tier, timestamp
                FROM coherence_profiles
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                variables = CoherenceVariables(psi=row[1], rho=row[2], q=row[3], f=row[4])
                profile = CoherenceProfile(
                    user_id=row[0],
                    variables=variables,
                    static_coherence=row[5],
                    coherence_velocity=0,
                    assessment_tier=row[6],
                    timestamp=datetime.fromisoformat(row[7])
                )
                profiles.append(profile)
        
        db.close()
        
        if not profiles:
            return jsonify({'error': 'No valid profiles found'}), 404
        
        # GPU-accelerated optimization
        recommendations, stats = accelerator.optimize_group_coherence(
            profiles, 
            target_coherence, 
            max_iterations
        )
        
        # Calculate group statistics
        current_avg = np.mean([p.static_coherence for p in profiles])
        target_avg = np.mean([r['target_coherence'] for r in recommendations])
        
        response = {
            'group_size': len(profiles),
            'current_average_coherence': float(current_avg),
            'target_coherence': target_coherence,
            'predicted_average_coherence': float(target_avg),
            'improvement_percentage': float((target_avg - current_avg) / current_avg * 100),
            'individual_recommendations': recommendations[:10],  # First 10
            'performance': {
                'gpu_time_ms': stats.gpu_time_ms,
                'speedup_factor': f"{stats.speedup_factor:.2f}x",
                'iterations_processed': stats.items_processed // len(profiles)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Group optimization error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@gpu_api.route('/gpu/performance_stats', methods=['GET'])
def performance_stats():
    """
    Get GPU acceleration performance statistics
    """
    try:
        summary = accelerator.get_performance_summary()
        return jsonify(summary)
    except Exception as e:
        logger.error(f"Performance stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@gpu_api.route('/gpu/benchmark', methods=['POST'])
def gpu_benchmark():
    """
    Run GPU acceleration benchmark
    """
    try:
        data = request.json
        test_sizes = data.get('test_sizes', [10, 100, 1000, 5000])
        
        results = []
        
        for size in test_sizes:
            # Generate test profiles
            test_profiles = []
            for i in range(size):
                variables = CoherenceVariables(
                    psi=np.random.random(),
                    rho=np.random.random(),
                    q=np.random.random(),
                    f=np.random.random()
                )
                profile = CoherenceProfile(
                    user_id=f"test_{i}",
                    variables=variables,
                    static_coherence=0,
                    coherence_velocity=0,
                    assessment_tier=1,
                    timestamp=datetime.now()
                )
                test_profiles.append(profile)
            
            # Run benchmark
            start = time.time()
            _, stats = accelerator.accelerate_coherence_batch(test_profiles, 'static_coherence')
            total_time = (time.time() - start) * 1000
            
            results.append({
                'batch_size': size,
                'total_time_ms': total_time,
                'per_item_us': (total_time * 1000) / size,  # microseconds
                'speedup': f"{stats.speedup_factor:.2f}x",
                'throughput_per_second': int(size / (total_time / 1000))
            })
        
        response = {
            'gpu_enabled': accelerator.gpu_available,
            'device_info': accelerator.device_info,
            'benchmark_results': results,
            'recommendation': 'Use batch sizes > 100 for optimal GPU utilization'
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"GPU benchmark error: {str(e)}")
        return jsonify({'error': str(e)}), 500