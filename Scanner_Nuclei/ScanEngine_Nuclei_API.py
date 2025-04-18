from flask import Flask, request, jsonify
import subprocess
import re
import requests
from urllib.parse import urlparse
from typing import List, Dict, Union, Tuple

app = Flask(__name__)

def is_valid_url_format(url: str) -> bool:
    """Checks if the URL has a proper format."""
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except ValueError:
        return False

def is_url_reachable(url: str) -> bool:
    """Sends a HEAD request to the URL to verify it is reachable."""
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code < 400
    except requests.RequestException:
        return False

def run_nuclei_scan(url: str, template: str) -> str:
    """Run a Nuclei scan with the given URL and template."""
    command = f"nuclei -u {url} -t {template}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout + "\n" + e.stderr

def filter_vulnerability_lines(output: str) -> List[str]:
    """Filter out only vulnerability detection lines from Nuclei output."""
    pattern = re.compile(r"^\[.+\] \[.+\] \[.+\] .+$")
    return [line for line in output.splitlines() if pattern.match(line)]

def strip_ansi_codes(text: str) -> str:
    """Remove ANSI color codes from the text."""
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def validate_url(url: str) -> Tuple[bool, str]:
    """Validate URL format and reachability."""
    if not url:
        return False, "URL parameter is missing"
    
    if not is_valid_url_format(url):
        return False, "Invalid URL format. Please provide a valid URL (e.g., http://example.com)"
    
    if not is_url_reachable(url):
        return False, "Could not reach the URL. Please check if the site is accessible"
    
    return True, ""

@app.route('/scan', methods=['POST'])
def scan() -> Tuple[Dict[str, Union[List[str], str]], int]:
    """
    API endpoint to perform Nuclei vulnerability scans on a target URL.
    
    Expected JSON request: {"url": "http://example.com"}
    Returns a list of detected vulnerabilities as strings.
    """
    # Get request data
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON request"}), 400
    
    url = data.get('url', '').strip()
    
    # Validate URL
    is_valid, error_message = validate_url(url)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    # Define templates to scan with
    templates = [
        "./juiceshop-admin-priv-escalation.yaml",
        "./juiceshop-ftp-exposure.yaml",
        "./juiceshop-sensitive-legal-file.yaml",
        "./juiceshop-sqli-login-bypass.yaml"
    ]
    
    # Run scans with all templates
    all_results = []
    for template in templates:
        app.logger.info(f"Running scan with template: {template} on {url}")
        output = run_nuclei_scan(url, template)
        vuln_lines = filter_vulnerability_lines(output)
        # Clean up the output by removing ANSI codes
        cleaned_lines = [strip_ansi_codes(line) for line in vuln_lines]
        all_results.extend(cleaned_lines)
    
    return jsonify({"vulnerabilities": all_results}), 200

@app.route('/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, str], int]:
    """Health check endpoint for monitoring."""
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
