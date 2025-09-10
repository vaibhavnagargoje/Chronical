# #!/usr/bin/env python3
# """
# Load Testing Script for Django Application
# Properly handles threading, rate limiting, and result tracking
# """

# import requests
# import time
# import threading
# import random
# import statistics
# from datetime import datetime
# from concurrent.futures import ThreadPoolExecutor, as_completed
# import sys
# import signal

# # Configuration
# TARGET_URL = "https://indiandistricts.in/maharashtra/"
# REQUESTS_PER_SECOND = 100  # Reduced from 500 to be more realistic
# DURATION = 30  # Test duration in seconds
# MAX_WORKERS = 10  # Maximum concurrent threads
# TIMEOUT = 10  # Request timeout in seconds

# # Results tracking with thread-safe operations
# class ResultTracker:
#     def __init__(self):
#         self.lock = threading.Lock()
#         self.success_count = 0
#         self.failure_count = 0
#         self.response_times = []
#         self.status_codes = {}
#         self.errors = {}
#         self.start_time = None
#         self.end_time = None
    
#     def add_success(self, response_time, status_code):
#         with self.lock:
#             self.success_count += 1
#             self.response_times.append(response_time)
#             self.status_codes[status_code] = self.status_codes.get(status_code, 0) + 1
    
#     def add_failure(self, error_type):
#         with self.lock:
#             self.failure_count += 1
#             self.errors[error_type] = self.errors.get(error_type, 0) + 1
    
#     def get_stats(self):
#         with self.lock:
#             total = self.success_count + self.failure_count
#             return {
#                 'total_requests': total,
#                 'successful': self.success_count,
#                 'failed': self.failure_count,
#                 'success_rate': (self.success_count / total * 100) if total > 0 else 0,
#                 'response_times': self.response_times.copy(),
#                 'status_codes': self.status_codes.copy(),
#                 'errors': self.errors.copy()
#             }

# # Global result tracker
# results = ResultTracker()
# stop_test = threading.Event()

# def make_single_request():
#     """Make a single HTTP request with proper error handling"""
#     request_start = time.time()
    
#     try:
#         # Add cache-busting parameter and user agent
#         params = {
#             'cache_bust': random.randint(1, 1000000),
#             'timestamp': int(time.time() * 1000)
#         }
        
#         headers = {
#             'User-Agent': 'LoadTest/1.0 (Python requests)',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.5',
#             'Accept-Encoding': 'gzip, deflate',
#             'Connection': 'keep-alive',
#         }
        
#         response = requests.get(
#             TARGET_URL,
#             params=params,
#             headers=headers,
#             timeout=TIMEOUT,
#             allow_redirects=True
#         )
        
#         response_time = time.time() - request_start
        
#         # Consider 2xx and 3xx as successful
#         if 200 <= response.status_code < 400:
#             results.add_success(response_time, response.status_code)
#         else:
#             results.add_failure(f"HTTP_{response.status_code}")
            
#     except requests.exceptions.Timeout:
#         results.add_failure("Timeout")
#     except requests.exceptions.ConnectionError:
#         results.add_failure("ConnectionError")
#     except requests.exceptions.RequestException as e:
#         results.add_failure(f"RequestException_{type(e).__name__}")
#     except Exception as e:
#         results.add_failure(f"UnknownError_{type(e).__name__}")

# def rate_limited_executor():
#     """Execute requests at specified rate"""
#     interval = 1.0 / REQUESTS_PER_SECOND
    
#     with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#         futures = []
#         start_time = time.time()
#         request_count = 0
        
#         while time.time() - start_time < DURATION and not stop_test.is_set():
#             # Submit request
#             future = executor.submit(make_single_request)
#             futures.append(future)
#             request_count += 1
            
#             # Rate limiting
#             next_request_time = start_time + (request_count * interval)
#             current_time = time.time()
            
#             if next_request_time > current_time:
#                 time.sleep(next_request_time - current_time)
            
#             # Print progress every 100 requests
#             if request_count % 100 == 0:
#                 stats = results.get_stats()
#                 print(f"Progress: {request_count} requests sent, "
#                       f"{stats['successful']} successful, "
#                       f"{stats['failed']} failed")
        
#         # Wait for all requests to complete
#         print("Waiting for remaining requests to complete...")
#         for future in as_completed(futures, timeout=TIMEOUT + 5):
#             try:
#                 future.result()
#             except:
#                 pass

# def signal_handler(signum, frame):
#     """Handle Ctrl+C gracefully"""
#     print("\nReceived interrupt signal. Stopping test...")
#     stop_test.set()
#     sys.exit(0)

# def print_detailed_results():
#     """Print comprehensive test results"""
#     stats = results.get_stats()
#     duration = results.end_time - results.start_time if results.end_time else 0
    
#     print("\n" + "="*60)
#     print("           LOAD TEST RESULTS")
#     print("="*60)
    
#     print(f"Target URL: {TARGET_URL}")
#     print(f"Test Duration: {duration:.2f} seconds")
#     print(f"Target Rate: {REQUESTS_PER_SECOND} requests/second")
#     print(f"Max Workers: {MAX_WORKERS}")
    
#     print(f"\nREQUEST SUMMARY:")
#     print(f"  Total Requests: {stats['total_requests']}")
#     print(f"  Successful: {stats['successful']}")
#     print(f"  Failed: {stats['failed']}")
#     print(f"  Success Rate: {stats['success_rate']:.2f}%")
    
#     if duration > 0:
#         actual_rate = stats['total_requests'] / duration
#         print(f"  Actual Rate: {actual_rate:.2f} requests/second")
    
#     # Response time statistics
#     if stats['response_times']:
#         response_times = stats['response_times']
#         print(f"\nRESPONSE TIME STATISTICS:")
#         print(f"  Average: {statistics.mean(response_times):.3f}s")
#         print(f"  Median: {statistics.median(response_times):.3f}s")
#         print(f"  Min: {min(response_times):.3f}s")
#         print(f"  Max: {max(response_times):.3f}s")
        
#         # Percentiles
#         sorted_times = sorted(response_times)
#         p95 = sorted_times[int(len(sorted_times) * 0.95)]
#         p99 = sorted_times[int(len(sorted_times) * 0.99)]
#         print(f"  95th percentile: {p95:.3f}s")
#         print(f"  99th percentile: {p99:.3f}s")
    
#     # Status codes
#     if stats['status_codes']:
#         print(f"\nSTATUS CODES:")
#         for code, count in sorted(stats['status_codes'].items()):
#             print(f"  {code}: {count} ({count/stats['total_requests']*100:.1f}%)")
    
#     # Errors
#     if stats['errors']:
#         print(f"\nERRORS:")
#         for error, count in sorted(stats['errors'].items()):
#             print(f"  {error}: {count} ({count/stats['total_requests']*100:.1f}%)")
    
#     print("="*60)

# def main():
#     """Main function to run the load test"""
#     # Set up signal handler for graceful shutdown
#     signal.signal(signal.SIGINT, signal_handler)
    
#     print(f"Load Test Configuration:")
#     print(f"  Target: {TARGET_URL}")
#     print(f"  Rate: {REQUESTS_PER_SECOND} requests/second")
#     print(f"  Duration: {DURATION} seconds")
#     print(f"  Max Workers: {MAX_WORKERS}")
#     print(f"  Timeout: {TIMEOUT} seconds")
#     print(f"  Expected Total Requests: {REQUESTS_PER_SECOND * DURATION}")
    
#     # Validate target URL
#     print(f"\nTesting connection to target...")
#     try:
#         test_response = requests.get(TARGET_URL, timeout=TIMEOUT)
#         print(f"✅ Connection successful (Status: {test_response.status_code})")
#     except Exception as e:
#         print(f"❌ Connection failed: {e}")
#         print("Please check the URL and try again.")
#         return
    
#     input("\nPress Enter to start the load test...")
    
#     results.start_time = time.time()
#     print(f"\n🚀 Starting load test at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     print("Press Ctrl+C to stop the test early\n")
    
#     try:
#         rate_limited_executor()
#     except KeyboardInterrupt:
#         print("\nTest interrupted by user")
#     except Exception as e:
#         print(f"\nTest failed with error: {e}")
#     finally:
#         results.end_time = time.time()
#         print_detailed_results()

# if __name__ == "__main__":
#     main()




#!/usr/bin/env python3
"""
Enhanced Load Testing Script for Django Application
With improved reporting, visualization, and error analysis
"""

import requests
import time
import threading
import random
import statistics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import signal
import json
import matplotlib.pyplot as plt
import numpy as np
from urllib.parse import urlparse

# Configuration
TARGET_URL = "https://indiandistricts.in/maharashtra/"
REQUESTS_PER_SECOND = 50  # Reduced to avoid overwhelming the server
DURATION = 60  # Test duration in seconds
MAX_WORKERS = 15  # Maximum concurrent threads
TIMEOUT = 15  # Request timeout in seconds

# Results tracking with thread-safe operations
class ResultTracker:
    def __init__(self):
        self.lock = threading.Lock()
        self.success_count = 0
        self.failure_count = 0
        self.response_times = []
        self.status_codes = {}
        self.errors = {}
        self.start_time = None
        self.end_time = None
        self.requests_sent = 0
        self.detailed_results = []
    
    def add_result(self, success, response_time=None, status_code=None, error_type=None, request_num=None):
        with self.lock:
            self.requests_sent += 1
            if success:
                self.success_count += 1
                self.response_times.append(response_time)
                self.status_codes[status_code] = self.status_codes.get(status_code, 0) + 1
                self.detailed_results.append({
                    'request_num': request_num,
                    'success': True,
                    'response_time': response_time,
                    'status_code': status_code,
                    'timestamp': time.time()
                })
            else:
                self.failure_count += 1
                self.errors[error_type] = self.errors.get(error_type, 0) + 1
                self.detailed_results.append({
                    'request_num': request_num,
                    'success': False,
                    'error_type': error_type,
                    'timestamp': time.time()
                })
    
    def get_stats(self):
        with self.lock:
            total = self.success_count + self.failure_count
            return {
                'total_requests': total,
                'requests_sent': self.requests_sent,
                'successful': self.success_count,
                'failed': self.failure_count,
                'success_rate': (self.success_count / total * 100) if total > 0 else 0,
                'completion_rate': (total / self.requests_sent * 100) if self.requests_sent > 0 else 0,
                'response_times': self.response_times.copy(),
                'status_codes': self.status_codes.copy(),
                'errors': self.errors.copy()
            }

# Global result tracker
results = ResultTracker()
stop_test = threading.Event()

def make_single_request(request_num):
    """Make a single HTTP request with proper error handling"""
    request_start = time.time()
    
    try:
        # Add cache-busting parameter and user agent
        params = {
            'cache_bust': random.randint(1, 1000000),
            'timestamp': int(time.time() * 1000)
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(
            TARGET_URL,
            params=params,
            headers=headers,
            timeout=TIMEOUT,
            allow_redirects=True
        )
        
        response_time = time.time() - request_start
        
        # Consider 2xx and 3xx as successful
        if 200 <= response.status_code < 400:
            results.add_result(True, response_time, response.status_code, None, request_num)
            return True, response_time, response.status_code
        else:
            results.add_result(False, None, None, f"HTTP_{response.status_code}", request_num)
            return False, None, f"HTTP_{response.status_code}"
            
    except requests.exceptions.Timeout:
        results.add_result(False, None, None, "Timeout", request_num)
        return False, None, "Timeout"
    except requests.exceptions.ConnectionError:
        results.add_result(False, None, None, "ConnectionError", request_num)
        return False, None, "ConnectionError"
    except requests.exceptions.RequestException as e:
        results.add_result(False, None, None, f"RequestException_{type(e).__name__}", request_num)
        return False, None, f"RequestException_{type(e).__name__}"
    except Exception as e:
        results.add_result(False, None, None, f"UnknownError_{type(e).__name__}", request_num)
        return False, None, f"UnknownError_{type(e).__name__}"

def rate_limited_executor():
    """Execute requests at specified rate"""
    interval = 1.0 / REQUESTS_PER_SECOND
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < DURATION and not stop_test.is_set():
            # Submit request
            future = executor.submit(make_single_request, request_count)
            futures.append(future)
            request_count += 1
            
            # Rate limiting
            next_request_time = start_time + (request_count * interval)
            current_time = time.time()
            
            if next_request_time > current_time:
                sleep_time = next_request_time - current_time
                time.sleep(sleep_time)
            
            # Print progress every 50 requests
            if request_count % 50 == 0:
                stats = results.get_stats()
                print(f"Progress: {stats['requests_sent']} requests sent, "
                      f"{stats['successful']} successful, "
                      f"{stats['failed']} failed")
        
        # Wait for all requests to complete with timeout
        print("Waiting for remaining requests to complete...")
        for future in as_completed(futures, timeout=TIMEOUT + 10):
            try:
                future.result(timeout=5)
            except:
                pass

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nReceived interrupt signal. Stopping test...")
    stop_test.set()
    sys.exit(0)

def generate_report():
    """Generate a comprehensive test report"""
    stats = results.get_stats()
    duration = results.end_time - results.start_time if results.end_time else 0
    
    report = {
        "test_configuration": {
            "target_url": TARGET_URL,
            "test_duration_seconds": DURATION,
            "request_rate_per_second": REQUESTS_PER_SECOND,
            "max_concurrent_workers": MAX_WORKERS,
            "request_timeout_seconds": TIMEOUT
        },
        "test_results": {
            "actual_duration_seconds": round(duration, 2),
            "total_requests_sent": stats['requests_sent'],
            "total_responses_received": stats['total_requests'],
            "successful_responses": stats['successful'],
            "failed_responses": stats['failed'],
            "success_rate_percent": round(stats['success_rate'], 2),
            "completion_rate_percent": round(stats['completion_rate'], 2),
            "actual_request_rate": round(stats['total_requests'] / duration, 2) if duration > 0 else 0
        },
        "response_times": {
            "average_seconds": round(statistics.mean(stats['response_times']), 3) if stats['response_times'] else 0,
            "median_seconds": round(statistics.median(stats['response_times']), 3) if stats['response_times'] else 0,
            "min_seconds": round(min(stats['response_times']), 3) if stats['response_times'] else 0,
            "max_seconds": round(max(stats['response_times']), 3) if stats['response_times'] else 0,
        },
        "status_codes": stats['status_codes'],
        "errors": stats['errors']
    }
    
    # Calculate percentiles if we have response times
    if stats['response_times']:
        sorted_times = sorted(stats['response_times'])
        report["response_times"]["p95_seconds"] = round(sorted_times[int(len(sorted_times) * 0.95)], 3)
        report["response_times"]["p99_seconds"] = round(sorted_times[int(len(sorted_times) * 0.99)], 3)
    
    return report

def visualize_results(report):
    """Create visualization of test results"""
    try:
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'Load Test Results for {urlparse(TARGET_URL).netloc}', fontsize=16)
        
        # Plot 1: Success vs Failed requests
        labels = ['Successful', 'Failed']
        values = [report['test_results']['successful_responses'], 
                 report['test_results']['failed_responses']]
        colors = ['#2ecc71', '#e74c3c']
        ax1.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Request Success Rate')
        
        # Plot 2: Response time distribution
        if report['test_results']['successful_responses'] > 0:
            response_times = results.get_stats()['response_times']
            ax2.hist(response_times, bins=20, color='#3498db', edgecolor='black')
            ax2.set_xlabel('Response Time (seconds)')
            ax2.set_ylabel('Frequency')
            ax2.set_title('Response Time Distribution')
        
        # Plot 3: Status codes
        if report['status_codes']:
            codes = list(report['status_codes'].keys())
            counts = list(report['status_codes'].values())
            ax3.bar([str(code) for code in codes], counts, color='#9b59b6')
            ax3.set_xlabel('HTTP Status Code')
            ax3.set_ylabel('Count')
            ax3.set_title('HTTP Status Codes')
        
        # Plot 4: Timeline of requests
        if results.detailed_results:
            timestamps = [r['timestamp'] for r in results.detailed_results if 'timestamp' in r]
            if timestamps:
                start_time = min(timestamps)
                relative_times = [t - start_time for t in timestamps]
                success = [1 if r['success'] else 0 for r in results.detailed_results if 'timestamp' in r]
                
                ax4.scatter(relative_times, success, alpha=0.6, color='#f39c12')
                ax4.set_xlabel('Time (seconds)')
                ax4.set_ylabel('Success (1=Yes, 0=No)')
                ax4.set_title('Request Success Over Time')
                ax4.set_yticks([0, 1])
                ax4.set_yticklabels(['Failed', 'Success'])
        
        plt.tight_layout()
        plt.savefig('load_test_results.png')
        print("Visualization saved as 'load_test_results.png'")
        
    except Exception as e:
        print(f"Could not generate visualization: {e}")

def print_detailed_results(report):
    """Print comprehensive test results"""
    print("\n" + "="*80)
    print("                     LOAD TEST RESULTS")
    print("="*80)
    
    print(f"Target URL: {report['test_configuration']['target_url']}")
    print(f"Test Duration: {report['test_results']['actual_duration_seconds']:.2f} seconds")
    print(f"Target Rate: {report['test_configuration']['request_rate_per_second']} requests/second")
    print(f"Max Workers: {report['test_configuration']['max_concurrent_workers']}")
    
    print(f"\nREQUEST SUMMARY:")
    print(f"  Total Requests Sent: {report['test_results']['total_requests_sent']}")
    print(f"  Total Responses Received: {report['test_results']['total_responses_received']}")
    print(f"  Successful Responses: {report['test_results']['successful_responses']}")
    print(f"  Failed Responses: {report['test_results']['failed_responses']}")
    print(f"  Success Rate: {report['test_results']['success_rate_percent']:.2f}%")
    print(f"  Completion Rate: {report['test_results']['completion_rate_percent']:.2f}%")
    
    if report['test_results']['actual_duration_seconds'] > 0:
        actual_rate = report['test_results']['actual_request_rate']
        print(f"  Actual Rate: {actual_rate:.2f} requests/second")
    
    # Response time statistics
    if report['test_results']['successful_responses'] > 0:
        print(f"\nRESPONSE TIME STATISTICS:")
        print(f"  Average: {report['response_times']['average_seconds']:.3f}s")
        print(f"  Median: {report['response_times']['median_seconds']:.3f}s")
        print(f"  Min: {report['response_times']['min_seconds']:.3f}s")
        print(f"  Max: {report['response_times']['max_seconds']:.3f}s")
        
        if 'p95_seconds' in report['response_times']:
            print(f"  95th percentile: {report['response_times']['p95_seconds']:.3f}s")
            print(f"  99th percentile: {report['response_times']['p99_seconds']:.3f}s")
    
    # Status codes
    if report['status_codes']:
        print(f"\nSTATUS CODES:")
        for code, count in sorted(report['status_codes'].items()):
            percentage = (count / report['test_results']['total_responses_received'] * 100) if report['test_results']['total_responses_received'] > 0 else 0
            print(f"  {code}: {count} ({percentage:.1f}%)")
    
    # Errors
    if report['errors']:
        print(f"\nERRORS:")
        for error, count in sorted(report['errors'].items()):
            percentage = (count / report['test_results']['total_responses_received'] * 100) if report['test_results']['total_responses_received'] > 0 else 0
            print(f"  {error}: {count} ({percentage:.1f}%)")
    
    print("="*80)

def save_report_to_file(report):
    """Save the report to a JSON file"""
    filename = f"load_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Detailed report saved to {filename}")

def main():
    """Main function to run the load test"""
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"Load Test Configuration:")
    print(f"  Target: {TARGET_URL}")
    print(f"  Rate: {REQUESTS_PER_SECOND} requests/second")
    print(f"  Duration: {DURATION} seconds")
    print(f"  Max Workers: {MAX_WORKERS}")
    print(f"  Timeout: {TIMEOUT} seconds")
    print(f"  Expected Total Requests: {REQUESTS_PER_SECOND * DURATION}")
    
    # Validate target URL
    print(f"\nTesting connection to target...")
    try:
        test_response = requests.get(TARGET_URL, timeout=TIMEOUT)
        print(f"✅ Connection successful (Status: {test_response.status_code})")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("Please check the URL and try again.")
        return
    
    input("\nPress Enter to start the load test...")
    
    results.start_time = time.time()
    print(f"\n🚀 Starting load test at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Press Ctrl+C to stop the test early\n")
    
    try:
        rate_limited_executor()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
    finally:
        results.end_time = time.time()
        report = generate_report()
        print_detailed_results(report)
        save_report_to_file(report)
        visualize_results(report)
        
        # Provide recommendations based on results
        print("\nRECOMMENDATIONS:")
        if report['test_results']['success_rate_percent'] < 90:
            print("❌ Your server may be struggling with the load. Consider:")
            print("   - Optimizing your application code")
            print("   - Implementing caching mechanisms")
            print("   - Scaling your infrastructure")
        elif report['test_results']['success_rate_percent'] < 99:
            print("⚠️  Your server is handling most requests but could be improved:")
            print("   - Check for occasional timeouts or errors")
            print("   - Consider implementing rate limiting")
        else:
            print("✅ Your server is handling the load excellently!")
            
        if report['response_times']['average_seconds'] > 2:
            print("❌ Response times are high. Consider:")
            print("   - Database query optimization")
            print("   - Implementing a CDN for static assets")
            print("   - Using a caching layer")

if __name__ == "__main__":
    main()