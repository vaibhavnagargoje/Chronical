#!/usr/bin/env python3
"""
Load Testing Script for Django Application
Properly handles threading, rate limiting, and result tracking
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

# Configuration
TARGET_URL = "http://159.65.158.177/cultural/maharashtra/ahilyanagar/architecture/"
REQUESTS_PER_SECOND = 100  # Reduced from 500 to be more realistic
DURATION =10  # Test duration in seconds
MAX_WORKERS = 50  # Maximum concurrent threads
TIMEOUT = 10  # Request timeout in seconds

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
    
    def add_success(self, response_time, status_code):
        with self.lock:
            self.success_count += 1
            self.response_times.append(response_time)
            self.status_codes[status_code] = self.status_codes.get(status_code, 0) + 1
    
    def add_failure(self, error_type):
        with self.lock:
            self.failure_count += 1
            self.errors[error_type] = self.errors.get(error_type, 0) + 1
    
    def get_stats(self):
        with self.lock:
            total = self.success_count + self.failure_count
            return {
                'total_requests': total,
                'successful': self.success_count,
                'failed': self.failure_count,
                'success_rate': (self.success_count / total * 100) if total > 0 else 0,
                'response_times': self.response_times.copy(),
                'status_codes': self.status_codes.copy(),
                'errors': self.errors.copy()
            }

# Global result tracker
results = ResultTracker()
stop_test = threading.Event()

def make_single_request():
    """Make a single HTTP request with proper error handling"""
    request_start = time.time()
    
    try:
        # Add cache-busting parameter and user agent
        params = {
            'cache_bust': random.randint(1, 1000000),
            'timestamp': int(time.time() * 1000)
        }
        
        headers = {
            'User-Agent': 'LoadTest/1.0 (Python requests)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
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
            results.add_success(response_time, response.status_code)
        else:
            results.add_failure(f"HTTP_{response.status_code}")
            
    except requests.exceptions.Timeout:
        results.add_failure("Timeout")
    except requests.exceptions.ConnectionError:
        results.add_failure("ConnectionError")
    except requests.exceptions.RequestException as e:
        results.add_failure(f"RequestException_{type(e).__name__}")
    except Exception as e:
        results.add_failure(f"UnknownError_{type(e).__name__}")

def rate_limited_executor():
    """Execute requests at specified rate"""
    interval = 1.0 / REQUESTS_PER_SECOND
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < DURATION and not stop_test.is_set():
            # Submit request
            future = executor.submit(make_single_request)
            futures.append(future)
            request_count += 1
            
            # Rate limiting
            next_request_time = start_time + (request_count * interval)
            current_time = time.time()
            
            if next_request_time > current_time:
                time.sleep(next_request_time - current_time)
            
            # Print progress every 100 requests
            if request_count % 100 == 0:
                stats = results.get_stats()
                print(f"Progress: {request_count} requests sent, "
                      f"{stats['successful']} successful, "
                      f"{stats['failed']} failed")
        
        # Wait for all requests to complete
        print("Waiting for remaining requests to complete...")
        for future in as_completed(futures, timeout=TIMEOUT + 5):
            try:
                future.result()
            except:
                pass

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nReceived interrupt signal. Stopping test...")
    stop_test.set()
    sys.exit(0)

def print_detailed_results():
    """Print comprehensive test results"""
    stats = results.get_stats()
    duration = results.end_time - results.start_time if results.end_time else 0
    
    print("\n" + "="*60)
    print("           LOAD TEST RESULTS")
    print("="*60)
    
    print(f"Target URL: {TARGET_URL}")
    print(f"Test Duration: {duration:.2f} seconds")
    print(f"Target Rate: {REQUESTS_PER_SECOND} requests/second")
    print(f"Max Workers: {MAX_WORKERS}")
    
    print(f"\nREQUEST SUMMARY:")
    print(f"  Total Requests: {stats['total_requests']}")
    print(f"  Successful: {stats['successful']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Success Rate: {stats['success_rate']:.2f}%")
    
    if duration > 0:
        actual_rate = stats['total_requests'] / duration
        print(f"  Actual Rate: {actual_rate:.2f} requests/second")
    
    # Response time statistics
    if stats['response_times']:
        response_times = stats['response_times']
        print(f"\nRESPONSE TIME STATISTICS:")
        print(f"  Average: {statistics.mean(response_times):.3f}s")
        print(f"  Median: {statistics.median(response_times):.3f}s")
        print(f"  Min: {min(response_times):.3f}s")
        print(f"  Max: {max(response_times):.3f}s")
        
        # Percentiles
        sorted_times = sorted(response_times)
        p95 = sorted_times[int(len(sorted_times) * 0.95)]
        p99 = sorted_times[int(len(sorted_times) * 0.99)]
        print(f"  95th percentile: {p95:.3f}s")
        print(f"  99th percentile: {p99:.3f}s")
    
    # Status codes
    if stats['status_codes']:
        print(f"\nSTATUS CODES:")
        for code, count in sorted(stats['status_codes'].items()):
            print(f"  {code}: {count} ({count/stats['total_requests']*100:.1f}%)")
    
    # Errors
    if stats['errors']:
        print(f"\nERRORS:")
        for error, count in sorted(stats['errors'].items()):
            print(f"  {error}: {count} ({count/stats['total_requests']*100:.1f}%)")
    
    print("="*60)

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
        print_detailed_results()

if __name__ == "__main__":
    main()