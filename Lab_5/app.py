#!/usr/bin/env python3
"""
Web Security Health Analyzer - MEDIUM LEVEL (Flask Web Application)
A simple web-based tool to analyze basic security aspects of a website.
"""

from flask import Flask, render_template, request
import requests
import time

# Initialize Flask application
app = Flask(__name__)

# ========================================
# HELPER FUNCTIONS
# ========================================


def validate_url(url):
    """
    Validate and format the URL.
    Adds https:// if no scheme is present.

    Args:
        url (str): The URL entered by user

    Returns:
        str: Formatted URL
    """
    url = url.strip()

    # Add https:// if no scheme provided
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def check_website(url):
    """
    Check if website is reachable and get response.

    Args:
        url (str): The URL to check

    Returns:
        tuple: (response object, error message)
               If successful: (response, None)
               If failed: (None, error_message)
    """
    try:
        # Set timeout to 10 seconds
        response = requests.get(url, timeout=10, allow_redirects=True)
        return response, None

    except requests.exceptions.Timeout:
        return None, "Request timed out after 10 seconds"

    except requests.exceptions.ConnectionError:
        return None, "Could not connect to the website"

    except requests.exceptions.RequestException as e:
        return None, f"Request failed: {str(e)}"

    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def measure_response_time(url):
    """
    Measure how long the website takes to respond.

    Args:
        url (str): The URL to measure

    Returns:
        float: Response time in milliseconds
    """
    try:
        start_time = time.time()
        requests.get(url, timeout=10, allow_redirects=True)
        end_time = time.time()

        # Convert to milliseconds
        response_time_ms = (end_time - start_time) * 1000
        return round(response_time_ms, 2)

    except:
        return None


def check_https(url):
    """
    Check if the website uses HTTPS protocol.

    Args:
        url (str): The URL to check

    Returns:
        bool: True if HTTPS, False otherwise
    """
    return url.startswith("https://")


def check_security_headers(response):
    """
    Check for presence of basic security headers.

    Args:
        response: The HTTP response object

    Returns:
        dict: Dictionary with header names as keys and their values/status
    """
    # List of security headers to check
    security_headers = {
        "Content-Security-Policy": None,
        "X-Frame-Options": None,
        "X-Content-Type-Options": None,
    }

    # Check each header
    for header in security_headers.keys():
        if header in response.headers:
            # Header is present - store its value
            security_headers[header] = response.headers[header]
        else:
            # Header is missing
            security_headers[header] = None

    return security_headers


# ========================================
# ROUTES
# ========================================


@app.route("/")
def home():
    """
    Home page route.
    Displays a form where user can enter website URL.
    """
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    """
    Scan route - handles form submission.
    Performs security analysis on the submitted URL.
    """
    # Get URL from form
    url_input = request.form.get("url", "").strip()

    # Check if URL is empty
    if not url_input:
        return render_template(
            "error.html",
            error_message="URL cannot be empty. Please enter a valid website URL.",
        )

    # Validate and format URL
    try:
        url = validate_url(url_input)
    except Exception as e:
        return render_template(
            "error.html", error_message=f"Invalid URL format: {str(e)}"
        )

    # Check if website is reachable
    response, error = check_website(url)

    if error:
        # Website is not reachable
        return render_template("error.html", error_message=error, url=url)

    # Perform all security checks
    status_code = response.status_code
    response_time = measure_response_time(url)
    uses_https = check_https(url)
    security_headers = check_security_headers(response)

    # Count how many security headers are present
    headers_present = sum(1 for value in security_headers.values() if value is not None)
    total_headers = len(security_headers)

    # Display results page
    return render_template(
        "results.html",
        url=url,
        status_code=status_code,
        response_time=response_time,
        uses_https=uses_https,
        security_headers=security_headers,
        headers_present=headers_present,
        total_headers=total_headers,
    )


# ========================================
# RUN APPLICATION
# ========================================

if __name__ == "__main__":
    # Run Flask development server
    # debug=True enables auto-reload and better error messages
    app.run(debug=True, host="0.0.0.0", port=5000)
