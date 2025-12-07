# Web Security Health Analyzer - MEDIUM LEVEL

This is a Flask web application that analyzes the security health of websites.

## Features

- ✓ Website reachability check
- ✓ HTTP status code display
- ✓ HTTPS usage verification
- ✓ Response time measurement
- ✓ Security headers check:
  - Content-Security-Policy
  - X-Frame-Options
  - X-Content-Type-Options

## Requirements

- Python 3.x
- Flask
- requests

## Installation

1. Install required packages:

```bash
pip install flask requests
```

## How to Run

1. Navigate to the Lab_5 directory:

```bash
cd "e:/RUET/CSE 3206/Lab_5"
```

2. Run the Flask application:

```bash
python app.py
```

3. Open your browser and go to:

```
http://localhost:5000
```

## Usage

1. Enter a website URL in the form (e.g., `example.com` or `https://example.com`)
2. Click "Scan Website"
3. View the security analysis results

## Project Structure

```
Lab_5/
├── app.py                          # Main Flask application
├── templates/
│   ├── index.html                  # Home page with input form
│   ├── results.html                # Results display page
│   └── error.html                  # Error page
└── README.md                       # This file
```

## Notes

- This is the MEDIUM LEVEL implementation (web-based)
- No database required
- No authentication needed
- Simple HTML templates with basic styling
