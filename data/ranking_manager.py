"""
Ranking Manager - Handles leaderboard data persistence
Adapted from Interactive Stand Game's DataManager (Phase 0)
"""

import json
import os
from typing import List, Dict
from config.app_config import LEADERBOARD_FILE


class RankingManager:
    """Manages leaderboard data persistence using JSON storage."""
    
    def __init__(self):
        """Initialize the ranking manager and ensure data file exists."""
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self) -> None:
        """Create the leaderboard file with empty structure if it doesn't exist."""
        if not os.path.exists(LEADERBOARD_FILE):
            # Create directory if needed
            os.makedirs(os.path.dirname(LEADERBOARD_FILE), exist_ok=True)
            
            # Create empty leaderboard file
            initial_data = {"scores": []}
            with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=4)
            print(f"Created new leaderboard file: {LEADERBOARD_FILE}")
    
    def load_leaderboard(self) -> List[Dict]:
        """
        Load the leaderboard data from JSON file.
        
        Returns:
            List of score dictionaries with keys: 'name', 'score', 'timestamp'
        """
        try:
            with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("scores", [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load {LEADERBOARD_FILE}: {e}")
            return []
    
    def save_leaderboard(self, scores_data: List[Dict]) -> bool:
        """
        Save the leaderboard data to JSON file using atomic write.
        
        Args:
            scores_data: List of score dictionaries
            
        Returns:
            True if save was successful, False otherwise
        """
        temp_file = LEADERBOARD_FILE + ".tmp"
        
        try:
            # Write to temporary file first
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump({"scores": scores_data}, f, indent=4, ensure_ascii=False)
            
            # Atomically rename temp file to final file (prevents corruption)
            os.replace(temp_file, LEADERBOARD_FILE)
            print(f"Leaderboard saved successfully ({len(scores_data)} entries)")
            return True
            
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
            
            # Clean up temp file if it exists
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
            
            return False
    
    def add_score(self, name: str, score: int, timestamp: str = None) -> bool:
        """
        Add a new score entry to the leaderboard.
        
        Args:
            name: Player name
            score: Score value
            timestamp: ISO format timestamp (auto-generated if None)
            
        Returns:
            True if score was added successfully
        """
        from datetime import datetime
        
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        # Load existing scores
        all_scores = self.load_leaderboard()
        
        # Add new score
        new_entry = {
            'name': name.strip().upper(),
            'score': score,
            'timestamp': timestamp
        }
        
        all_scores.append(new_entry)
        
        # Save updated leaderboard
        return self.save_leaderboard(all_scores)
    
    def get_top_scores(self, limit: int = 10) -> List[Dict]:
        """
        Get top N scores sorted by score (descending).
        
        Args:
            limit: Number of top scores to return
            
        Returns:
            List of top score entries
        """
        all_scores = self.load_leaderboard()
        sorted_scores = sorted(all_scores, key=lambda x: x['score'], reverse=True)
        return sorted_scores[:limit]
    
    def get_today_scores(self) -> List[Dict]:
        """
        Get all scores from today only.
        
        Returns:
            List of today's score entries
        """
        from datetime import datetime
        
        all_scores = self.load_leaderboard()
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        today_scores = []
        for score in all_scores:
            timestamp_str = score.get('timestamp', '')
            if timestamp_str:
                # Extract date from ISO timestamp (YYYY-MM-DDTHH:MM:SS)
                score_date = timestamp_str.split('T')[0]
                if score_date == current_date:
                    today_scores.append(score)
        
        return today_scores