#!/usr/bin/env python3
"""
Test script to verify the ranking_manager.py fix for AttributeError
"""

import json
import os
import sys
from data.ranking_manager import RankingManager

def test_ranking_manager():
    """Test the ranking manager with both list and dict formats"""
    
    print("=" * 60)
    print("Testing RankingManager Fix")
    print("=" * 60)
    
    # Initialize manager
    manager = RankingManager()
    
    # Test 1: Load existing data (should be a list format currently)
    print("\n[Test 1] Loading existing leaderboard...")
    scores = manager.load_leaderboard()
    print(f"✓ Loaded successfully: {scores}")
    print(f"  Type: {type(scores)}")
    print(f"  Length: {len(scores)}")
    
    # Test 2: Add a score
    print("\n[Test 2] Adding a test score...")
    success = manager.add_score("TEST USER", 9500, "2025-10-26T21:00:00")
    if success:
        print("✓ Score added successfully")
    else:
        print("✗ Failed to add score")
        return False
    
    # Test 3: Verify the file format after save
    print("\n[Test 3] Verifying file format after save...")
    with open('data/leaderboard.json', 'r') as f:
        file_data = json.load(f)
    print(f"  File contains: {type(file_data)}")
    if isinstance(file_data, dict) and "scores" in file_data:
        print("✓ File saved in correct dict format with 'scores' key")
        print(f"  Scores in file: {file_data['scores']}")
    else:
        print("✗ File not in expected format")
        return False
    
    # Test 4: Load again (now should handle dict format)
    print("\n[Test 4] Loading leaderboard again (dict format)...")
    scores = manager.load_leaderboard()
    print(f"✓ Loaded successfully: {scores}")
    print(f"  Found {len(scores)} score(s)")
    
    # Test 5: Get top scores
    print("\n[Test 5] Getting top scores...")
    top_scores = manager.get_top_scores(limit=5)
    print(f"✓ Retrieved {len(top_scores)} top score(s)")
    for i, score in enumerate(top_scores, 1):
        print(f"  {i}. {score['name']}: {score['score']}")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_ranking_manager()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)