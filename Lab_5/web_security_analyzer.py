#!/usr/bin/env python3
# Web Security Health Analyzer - LOW LEVEL

import requests
import time

# Main program
print("\n" + "=" * 50)
print("WEB SECURITY HEALTH ANALYZER")
print("=" * 50)

# Get URL from user
url = input("\nEnter website URL: ").strip()

# Add https:// if not present
if not url.startswith(("http://", "https://")):
    url = "https://" + url

print(f"\nAnalyzing: {url}")
print("Please wait...\n")

# Try to connect to website
try:
    start_time = time.time()
    response = requests.get(url, timeout=10)
    response_time = (time.time() - start_time) * 1000

    # Print results
    print("=" * 50)
    print("RESULTS")
    print("=" * 50)

    # 1. Reachability
    print("\n[1] Website Status: REACHABLE")

    # 2. HTTP Status Code
    print(f"[2] HTTP Status Code: {response.status_code}")

    # 3. HTTPS Check
    uses_https = url.startswith("https://")
    print(f"[3] HTTPS: {'YES' if uses_https else 'NO'}")

    # 4. Response Time
    print(f"[4] Response Time: {response_time:.2f} ms")

    # 5. Security Headers
    print("\n[5] SECURITY HEADERS:")
    headers = ["Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options"]

    for header in headers:
        if header in response.headers:
            print(f"    {header}: PRESENT")
        else:
            print(f"    {header}: MISSING")

    print("\n" + "=" * 50 + "\n")

except requests.exceptions.Timeout:
    print("ERROR: Request timed out")
except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect to website")
except Exception as e:
    print(f"ERROR: {str(e)}")
