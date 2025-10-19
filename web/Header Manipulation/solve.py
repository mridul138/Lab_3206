
#!/usr/bin/env python3
"""
solve.py
Simple solver that tries multiple HTTP methods looking for the flag.
It checks both response body and response headers for a CTF-style flag.

Usage:
    python3 solve.py https://example.com/target-path
"""

import sys
import re
from urllib.parse import urlparse
import requests

# Methods to try (ordered)
METHODS = ["GET", "POST", "HEAD", "PUT", "TRACE", "OPTIONS", "PATCH", "DELETE"]

FLAG_RE = re.compile(r"CTF\{.*?\}")

def try_method(url, method, timeout=5):
    try:
        # For HEAD we don't expect a body, but we'll still inspect headers.
        resp = requests.request(method, url, timeout=timeout, allow_redirects=False)
    except requests.RequestException as e:
        print(f"[!] {method} -> request failed: {e}")
        return None

    # Collect results
    info = {
        "method": method,
        "status_code": resp.status_code,
        "headers": dict(resp.headers),
        "text": resp.text if method != "HEAD" else "",
    }
    return info

def scan_for_flag(info):
    # 1) Check response body
    text = info.get("text", "")
    m = FLAG_RE.search(text)
    if m:
        return ("body", m.group(0))

    # 2) Check common header names
    for h_name, h_val in info.get("headers", {}).items():
        if FLAG_RE.search(h_val):
            return (f"header:{h_name}", FLAG_RE.search(h_val).group(0))

    # 3) Generic header search (if header value may contain flag-like text)
    for h_name, h_val in info.get("headers", {}).items():
        if FLAG_RE.search(h_val):
            return (f"header:{h_name}", FLAG_RE.search(h_val).group(0))

    return None

def main(argv):
    if len(argv) != 2:
        print("Usage: python3 solve.py <url>")
        sys.exit(2)

    url = argv[1]
    # quick sanity check
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        print("[!] Invalid URL. Include scheme (http:// or https://).")
        sys.exit(2)

    print(f"[+] Scanning {url} with methods: {', '.join(METHODS)}")

    for method in METHODS:
        print(f"[.] Trying {method} ... ", end="", flush=True)
        info = try_method(url, method)
        if info is None:
            print("failed")
            continue

        print(f"HTTP {info['status_code']}")
        found = scan_for_flag(info)
        if found:
            where, flag = found
            print(f"\n[***] FLAG FOUND using {method} ({where}) --> {flag}\n")
            return

    print("\n[-] No flag found using methods:", ", ".join(METHODS))
    print("[*] Try additional methods or inspect responses manually.")

if __name__ == "__main__":
    main(sys.argv)
