# Header Manipulation — Demo CTF (Writeup)

**Category:** Web / Header Manipulation  
**Difficulty:** Easy  
**Points:** 100

## Problem statement (for players)
A hidden flag can be obtained by interacting with the web server using the correct HTTP method. The server behaves normally for most methods — but one method returns the flag.

You may try various HTTP request methods (GET, POST, HEAD, PUT, TRACE, OPTIONS, etc.). The flag may appear in the response body or in a response header.

> **Note (challenge authors):** this repository contains a demo solver and a public writeup. Do not use this if you want the challenge to remain unsolved in future competitions.

## Objective
Find the correct HTTP method and retrieve the flag.

## Hints
- Try different HTTP methods — some servers treat methods differently.
- Inspect both response body **and** response headers (e.g., `X-Flag`, `X-Secret`).
- Tools: `curl -X METHOD`, Burp, or the included `solve.py`.

## Flag format
Flags follow the format: `CTF{...}`

## Example usage (solver)
```bash
python3 solve.py https://example.com/target-path
