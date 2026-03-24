import difflib
from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple, Optional

class DiffFlow:
    def __init__(self, max_workers: Optional[int] = None):
        self.max_workers = max_workers
    
    def compare_strings(self, str1: str, str2: str) -> List[str]:
        """Compare two strings and return diff in unified format"""
        diff = difflib.unified_diff(
            str1.splitlines(keepends=True),
            str2.splitlines(keepends=True)
        )
        return list(diff)
    
    def batch_compare(self, pairs: List[Tuple[str, str]]) -> List[List[str]]:
        """Compare multiple pairs of strings in parallel
        
        Args:
            pairs: List of (str1, str2) tuples to compare
            
        Returns:
            List of diffs for each pair
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(
                lambda p: self.compare_strings(p[0], p[1]),
                pairs
            ))
        return results
    
    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity score between two strings
        
        Returns float between 0 (completely different) and 1 (identical)
        """
        matcher = difflib.SequenceMatcher(None, str1, str2)
        return matcher.ratio()
    
    def batch_similarity(self, pairs: List[Tuple[str, str]]) -> List[float]:
        """Calculate similarity scores for multiple string pairs in parallel"""
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            scores = list(executor.map(
                lambda p: self.similarity_score(p[0], p[1]),
                pairs
            ))
        return scores
    
    def find_closest_match(self, target: str, candidates: List[str]) -> Tuple[str, float]:
        """Find the closest matching string from a list of candidates
        
        Returns:
            Tuple of (best_match, similarity_score)
        """
        scores = self.batch_similarity([(target, c) for c in candidates])
        best_idx = max(range(len(scores)), key=scores.__getitem__)
        return candidates[best_idx], scores[best_idx]
