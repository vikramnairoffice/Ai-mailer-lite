"""
SMTP account scoring and ranking engine for Email Marketing System
"""

import random
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
import logging

from .gmass_automation import GmassTestResult

class ScoringEngine:
    """SMTP account scoring and ranking system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.score_weights = {
            'inbox_score': 0.6,      # 60% weight for inbox delivery
            'spam_score': -0.3,      # 30% penalty for spam folder
            'promotional_score': 0.1  # 10% weight for promotional folder
        }
    
    def calculate_smtp_score(self, test_results: List[GmassTestResult]) -> Dict[str, Any]:
        """Calculate overall score for an SMTP account"""
        if not test_results:
            return self._get_default_score()
        
        # Calculate averages
        total_tests = len(test_results)
        avg_inbox = sum(r.inbox_score for r in test_results) / total_tests
        avg_spam = sum(r.spam_score for r in test_results) / total_tests
        avg_promo = sum(r.promotional_score for r in test_results) / total_tests
        
        # Calculate weighted score
        weighted_score = (
            avg_inbox * self.score_weights['inbox_score'] +
            avg_spam * self.score_weights['spam_score'] +
            avg_promo * self.score_weights['promotional_score']
        )
        
        # Normalize to 0-100 scale
        final_score = max(0, min(100, weighted_score))
        
        # Determine grade based on score
        grade = self._calculate_grade(final_score)
        
        # Calculate reliability score based on consistency
        reliability = self._calculate_reliability(test_results)
        
        return {
            'smtp_account': test_results[0].smtp_account if test_results else '',
            'overall_score': round(final_score, 2),
            'grade': grade,
            'reliability': reliability,
            'avg_inbox_score': round(avg_inbox, 2),
            'avg_spam_score': round(avg_spam, 2),
            'avg_promotional_score': round(avg_promo, 2),
            'total_tests': total_tests,
            'last_tested': max(r.tested_at for r in test_results),
            'recommendation': self._get_recommendation(final_score, reliability)
        }
    
    def rank_smtp_accounts(self, smtp_scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank SMTP accounts by their scores"""
        # Sort by overall score (descending) and reliability (descending)
        ranked = sorted(
            smtp_scores,
            key=lambda x: (x['overall_score'], x['reliability']),
            reverse=True
        )
        
        # Add ranking position
        for i, account in enumerate(ranked, 1):
            account['rank'] = i
            account['rank_category'] = self._get_rank_category(i, len(ranked))
        
        return ranked
    
    def get_best_smtp_accounts(self, smtp_scores: List[Dict[str, Any]], 
                              limit: int = 5, min_score: float = 50.0) -> List[Dict[str, Any]]:
        """Get the best performing SMTP accounts"""
        # Filter accounts with minimum score
        qualified = [
            account for account in smtp_scores 
            if account['overall_score'] >= min_score
        ]
        
        # Rank and return top performers
        ranked = self.rank_smtp_accounts(qualified)
        return ranked[:limit]
    
    def simulate_smtp_test(self, smtp_email: str, test_emails: List[str]) -> List[GmassTestResult]:
        """Simulate SMTP testing for development/demo purposes"""
        results = []
        
        # Generate realistic but random test results
        base_inbox_score = random.uniform(60, 95)
        base_spam_score = random.uniform(5, 30)
        base_promo_score = random.uniform(0, 15)
        
        for test_email in test_emails:
            # Add some variation to each test
            inbox_score = max(0, min(100, base_inbox_score + random.uniform(-10, 10)))
            spam_score = max(0, min(100, base_spam_score + random.uniform(-5, 5)))
            promo_score = max(0, min(100, base_promo_score + random.uniform(-3, 3)))
            
            # Calculate total score
            total_score = inbox_score - spam_score + (promo_score * 0.5)
            
            result = GmassTestResult(
                email_address=test_email,
                smtp_account=smtp_email,
                inbox_score=int(inbox_score),
                spam_score=int(spam_score),
                promotional_score=int(promo_score),
                total_score=int(total_score),
                test_details={
                    'delivery_time': random.uniform(1.0, 5.0),
                    'reputation_score': random.uniform(7.0, 9.5),
                    'content_score': random.uniform(6.0, 9.0)
                },
                tested_at=datetime.now(),
                success=total_score > 30,
                error_message=None if total_score > 30 else "Low deliverability detected"
            )
            
            results.append(result)
        
        return results
    
    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade based on score"""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        elif score >= 40:
            return 'D'
        else:
            return 'F'
    
    def _calculate_reliability(self, test_results: List[GmassTestResult]) -> float:
        """Calculate reliability score based on result consistency"""
        if len(test_results) < 2:
            return 100.0  # Single test assumed reliable
        
        # Calculate variance in total scores
        scores = [r.total_score for r in test_results]
        mean_score = sum(scores) / len(scores)
        variance = sum((x - mean_score) ** 2 for x in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # Convert to reliability percentage (lower variance = higher reliability)
        reliability = max(0, 100 - (std_dev * 2))
        return round(reliability, 2)
    
    def _get_recommendation(self, score: float, reliability: float) -> str:
        """Get recommendation based on score and reliability"""
        if score >= 80 and reliability >= 80:
            return "Excellent - Use for high-priority campaigns"
        elif score >= 70 and reliability >= 70:
            return "Good - Suitable for regular campaigns"
        elif score >= 60:
            return "Fair - Use with caution, monitor results"
        elif score >= 50:
            return "Poor - Consider improving or replacing"
        else:
            return "Critical - Do not use for important campaigns"
    
    def _get_rank_category(self, rank: int, total: int) -> str:
        """Get rank category description"""
        percentile = (rank / total) * 100
        
        if percentile <= 10:
            return "Top Tier"
        elif percentile <= 25:
            return "High Performer"
        elif percentile <= 50:
            return "Above Average"
        elif percentile <= 75:
            return "Average"
        else:
            return "Below Average"
    
    def _get_default_score(self) -> Dict[str, Any]:
        """Get default score for accounts with no test results"""
        return {
            'smtp_account': '',
            'overall_score': 0.0,
            'grade': 'F',
            'reliability': 0.0,
            'avg_inbox_score': 0.0,
            'avg_spam_score': 100.0,
            'avg_promotional_score': 0.0,
            'total_tests': 0,
            'last_tested': None,
            'recommendation': "Not tested - run inbox test first"
        }