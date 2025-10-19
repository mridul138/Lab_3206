# Writeup — Header Manipulation Demo

## Quick summary
This challenge required interacting with the target URL using different HTTP methods. While common methods (GET and POST) returned normal content, one of the less commonly used methods returned the flag — either in the response body or in a custom response header.

## Steps taken
1. Manually tested with `curl`:
   - `curl -i -X GET https://target/` — ordinary content, no flag.
   - `curl -i -X POST https://target/` — ordinary content, no flag.
   - `curl -i -X HEAD https://target/` — headers only; nothing obvious.
   - `curl -i -X TRACE https://target/` — returned a response containing the flag header `X-Flag: CTF{...}` (example).

2. Wrote `solve.py` to automate trying a list of methods and look for `CTF{...}` in both body and headers.

3. Extracted flag when server responded to the correct method (e.g., `TRACE`) and provided the flag in the header `X-Flag` (or in the body).

## Why this worked (root cause)
Some web servers or custom application code handle different HTTP methods differently. The endpoint was configured to return sensitive information only on a non-standard method (e.g., TRACE/PUT/OPTIONS), perhaps for debugging or misconfiguration reasons. Attackers can enumerate HTTP methods to find such leaks.

## Mitigation / Fix
- Ensure endpoints return consistent behavior across methods and only allow methods required by the application (typically `GET`, `POST` — avoid enabling `TRACE`, `PUT`, `DELETE`, etc., unless needed).
- Disable HTTP methods like `TRACE` at the web server or WAF level if not used.
- Never place secrets or flags in response headers, debug endpoints, or developer-only paths.
- Apply least privilege: endpoints that reveal sensitive state should require proper authentication and authorization.

## Detection
- Monitor logs for unusual methods (TRACE/PUT/DELETE/OPTIONS) being used against public endpoints.
- Add automated tests to verify no secrets are exposed via headers or uncommon methods.

## Final note
This is a demonstration of header/method enumeration and why restricting/monitoring HTTP verbs and response headers is important. The included `solve.py` is meant as an educational automation helper — keep it for learning or testing in safe/authorized environments only.
