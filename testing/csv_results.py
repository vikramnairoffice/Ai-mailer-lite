"""
CSV-based result storage for GMass testing (no database)
"""

import os
import csv
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

from .gmass_automation import GmassTestResult

class CSVResultsManager:
    """Manage GMass test results using CSV files"""
    
    def __init__(self, results_dir: str = "test_results"):
        self.logger = logging.getLogger(__name__)
        self.results_dir = results_dir
        self.ensure_results_directory()
        
    def ensure_results_directory(self) -> None:
        """Ensure results directory exists"""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
            
    def save_test_result(self, result: GmassTestResult) -> bool:
        """Save a single test result to CSV"""
        try:
            filename = self._get_results_filename(result.smtp_account)
            file_exists = os.path.exists(filename)
            
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'email_address', 'smtp_account', 'inbox_score', 'spam_score', 
                    'promotional_score', 'total_score', 'tested_at', 'success', 
                    'error_message', 'delivery_time', 'reputation_score', 'content_score'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header if file is new
                if not file_exists:
                    writer.writeheader()
                
                # Prepare row data
                row_data = {
                    'email_address': result.email_address,
                    'smtp_account': result.smtp_account,
                    'inbox_score': result.inbox_score,
                    'spam_score': result.spam_score,
                    'promotional_score': result.promotional_score,
                    'total_score': result.total_score,
                    'tested_at': result.tested_at.isoformat(),
                    'success': result.success,
                    'error_message': result.error_message or '',
                    'delivery_time': result.test_details.get('delivery_time', ''),
                    'reputation_score': result.test_details.get('reputation_score', ''),
                    'content_score': result.test_details.get('content_score', '')
                }
                
                writer.writerow(row_data)
                
            self.logger.info(f"Saved test result for {result.smtp_account}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving test result: {e}")
            return False
    
    def save_multiple_results(self, results: List[GmassTestResult]) -> int:
        """Save multiple test results and return count of successful saves"""
        saved_count = 0
        
        for result in results:
            if self.save_test_result(result):
                saved_count += 1
                
        return saved_count
    
    def load_smtp_results(self, smtp_account: str) -> List[GmassTestResult]:
        """Load all test results for a specific SMTP account"""
        filename = self._get_results_filename(smtp_account)
        results = []
        
        if not os.path.exists(filename):
            return results
            
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    result = GmassTestResult(
                        email_address=row['email_address'],
                        smtp_account=row['smtp_account'],
                        inbox_score=int(row['inbox_score']) if row['inbox_score'] else 0,
                        spam_score=int(row['spam_score']) if row['spam_score'] else 0,
                        promotional_score=int(row['promotional_score']) if row['promotional_score'] else 0,
                        total_score=int(row['total_score']) if row['total_score'] else 0,
                        test_details={
                            'delivery_time': row.get('delivery_time', ''),
                            'reputation_score': row.get('reputation_score', ''),
                            'content_score': row.get('content_score', '')
                        },
                        tested_at=datetime.fromisoformat(row['tested_at']),
                        success=row['success'].lower() == 'true',
                        error_message=row['error_message'] if row['error_message'] else None
                    )
                    results.append(result)
                    
        except Exception as e:
            self.logger.error(f"Error loading results for {smtp_account}: {e}")
            
        return results
    
    def get_recent_results(self, smtp_account: str, days: int = 7) -> List[GmassTestResult]:
        """Get recent test results for an SMTP account"""
        all_results = self.load_smtp_results(smtp_account)
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_results = [
            result for result in all_results 
            if result.tested_at >= cutoff_date
        ]
        
        return recent_results
    
    def get_all_smtp_accounts(self) -> List[str]:
        """Get list of all SMTP accounts that have test results"""
        smtp_accounts = []
        
        if not os.path.exists(self.results_dir):
            return smtp_accounts
            
        for filename in os.listdir(self.results_dir):
            if filename.endswith('_results.csv'):
                # Extract SMTP account from filename
                smtp_account = filename.replace('_results.csv', '').replace('_', '@', 1)
                smtp_accounts.append(smtp_account)
                
        return smtp_accounts
    
    def export_summary_report(self, output_filename: str = None) -> str:
        """Export summary report of all SMTP accounts"""
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"smtp_summary_report_{timestamp}.csv"
            
        try:
            with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'smtp_account', 'total_tests', 'avg_inbox_score', 'avg_spam_score',
                    'avg_promotional_score', 'avg_total_score', 'success_rate', 
                    'last_tested', 'recommendation'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                # Process each SMTP account
                for smtp_account in self.get_all_smtp_accounts():
                    results = self.load_smtp_results(smtp_account)
                    if results:
                        summary = self._calculate_account_summary(smtp_account, results)
                        writer.writerow(summary)
                        
            self.logger.info(f"Summary report exported to {output_filename}")
            return output_filename
            
        except Exception as e:
            self.logger.error(f"Error exporting summary report: {e}")
            return ""
    
    def cleanup_old_results(self, days: int = 30) -> int:
        """Clean up test results older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        cleaned_count = 0
        
        for smtp_account in self.get_all_smtp_accounts():
            results = self.load_smtp_results(smtp_account)
            recent_results = [
                result for result in results 
                if result.tested_at >= cutoff_date
            ]
            
            if len(recent_results) < len(results):
                # Rewrite file with only recent results
                filename = self._get_results_filename(smtp_account)
                try:
                    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                        fieldnames = [
                            'email_address', 'smtp_account', 'inbox_score', 'spam_score',
                            'promotional_score', 'total_score', 'tested_at', 'success',
                            'error_message', 'delivery_time', 'reputation_score', 'content_score'
                        ]
                        
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        
                        for result in recent_results:
                            row_data = {
                                'email_address': result.email_address,
                                'smtp_account': result.smtp_account,
                                'inbox_score': result.inbox_score,
                                'spam_score': result.spam_score,
                                'promotional_score': result.promotional_score,
                                'total_score': result.total_score,
                                'tested_at': result.tested_at.isoformat(),
                                'success': result.success,
                                'error_message': result.error_message or '',
                                'delivery_time': result.test_details.get('delivery_time', ''),
                                'reputation_score': result.test_details.get('reputation_score', ''),
                                'content_score': result.test_details.get('content_score', '')
                            }
                            writer.writerow(row_data)
                            
                    cleaned_count += len(results) - len(recent_results)
                    
                except Exception as e:
                    self.logger.error(f"Error cleaning results for {smtp_account}: {e}")
                    
        return cleaned_count
    
    def _get_results_filename(self, smtp_account: str) -> str:
        """Get CSV filename for SMTP account results"""
        # Replace @ with _ for filename safety
        safe_name = smtp_account.replace('@', '_')
        return os.path.join(self.results_dir, f"{safe_name}_results.csv")
    
    def _calculate_account_summary(self, smtp_account: str, 
                                  results: List[GmassTestResult]) -> Dict[str, Any]:
        """Calculate summary statistics for an SMTP account"""
        if not results:
            return {}
            
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r.success)
        
        return {
            'smtp_account': smtp_account,
            'total_tests': total_tests,
            'avg_inbox_score': round(sum(r.inbox_score for r in results) / total_tests, 2),
            'avg_spam_score': round(sum(r.spam_score for r in results) / total_tests, 2),
            'avg_promotional_score': round(sum(r.promotional_score for r in results) / total_tests, 2),
            'avg_total_score': round(sum(r.total_score for r in results) / total_tests, 2),
            'success_rate': round((successful_tests / total_tests) * 100, 2),
            'last_tested': max(r.tested_at for r in results).isoformat(),
            'recommendation': self._get_account_recommendation(results)
        }
    
    def _get_account_recommendation(self, results: List[GmassTestResult]) -> str:
        """Get recommendation based on account performance"""
        if not results:
            return "No data available"
            
        avg_total_score = sum(r.total_score for r in results) / len(results)
        success_rate = sum(1 for r in results if r.success) / len(results) * 100
        
        if avg_total_score >= 70 and success_rate >= 80:
            return "Excellent"
        elif avg_total_score >= 50 and success_rate >= 70:
            return "Good"
        elif avg_total_score >= 30:
            return "Fair"
        else:
            return "Poor"