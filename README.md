# Nuclei Scan Engine

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Supported Vulnerability Checks](#supported-vulnerability-checks)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Deployment](#deployment)
- [API Usage](#api-usage)
  - [Vulnerability Scan](#vulnerability-scan)
  - [Health Check](#health-check)
- [Custom Templates](#custom-templates)
- [Architecture](#architecture)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Template Customization](#template-customization)
- [Error Handling](#error-handling)
- [Security Considerations](#security-considerations)
- [Development](#development)
  - [Local Development](#local-development)
  - [Adding New Templates](#adding-new-templates)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Disclaimer](#disclaimer)

## Overview

A containerized vulnerability scanning service powered by Nuclei, specifically designed for testing OWASP Juice Shop applications. This service provides a REST API interface for running automated security scans using custom Nuclei templates.

## Features

- **REST API Interface**: Simple HTTP endpoints for vulnerability scanning
- **Custom Nuclei Templates**: Pre-configured templates for common Juice Shop vulnerabilities
- **Dockerized Deployment**: Easy setup and deployment using Docker
- **URL Validation**: Built-in URL format and reachability validation
- **Health Monitoring**: Health check endpoint for service monitoring
- **Clean Output**: Filtered and sanitized scan results

## Supported Vulnerability Checks

The scanner includes custom Nuclei templates for detecting:

- **Admin Privilege Escalation**: Checks for unauthorized admin role assignments
- **FTP Directory Exposure**: Detects exposed FTP directories with sensitive files
- **Sensitive Legal File Disclosure**: Identifies exposed legal documentation
- **SQL Injection Login Bypass**: Tests for authentication bypass vulnerabilities

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Deployment

1. Clone the repository:
```bash
git clone <repository-url>
cd nuclei-scan-engine/
```

2. Build and start the service:
```bash
docker-compose up --build
```

The service will be available at `http://localhost:5000`

## API Usage

### Vulnerability Scan

**Endpoint**: `POST /scan`

**Request Body**:
```json
{
  "url": "http://example.com"
}
```

**Response**:
```json
{
  "vulnerabilities": [
    "[2025-06-29 10:30:45] [juice-shop-sqli-login-bypass] [high] http://example.com/#/login",
    "[2025-06-29 10:30:46] [juiceshop-ftp-exposure] [medium] http://example.com/ftp"
  ]
}
```

**Example Usage**:
```bash
curl -X POST http://localhost:5000/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "http://localhost:3000"}'
```

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "ok"
}
```

## Custom Templates

The scanner uses four custom Nuclei templates located in the `Scanner_Nuclei/` directory:

### 1. Admin Privilege Escalation (`juiceshop-admin-priv-escalation.yaml`)
- **Severity**: High
- **Description**: Detects unauthorized admin role assignments
- **Method**: Checks user API endpoints for admin privileges

### 2. FTP Directory Exposure (`juiceshop-ftp-exposure.yaml`)
- **Severity**: Medium
- **Description**: Identifies exposed FTP directories
- **Method**: Scans for accessible `/ftp` endpoints

### 3. Sensitive Legal File (`juiceshop-sensitive-legal-file.yaml`)
- **Severity**: Medium
- **Description**: Detects exposed legal documentation
- **Method**: Checks for accessible `legal.md` files

### 4. SQL Injection Login Bypass (`juiceshop-sqli-login-bypass.yaml`)
- **Severity**: High
- **Description**: Tests for authentication bypass via SQL injection
- **Method**: Attempts login bypass using SQL injection payloads

## Architecture

The application consists of:

- **Flask API Server**: Handles HTTP requests and orchestrates scans
- **Nuclei Scanner**: Core vulnerability scanning engine
- **Custom Templates**: Specialized detection rules for Juice Shop
- **Docker Container**: Isolated runtime environment

## Configuration

### Environment Variables

The service can be configured using the following environment variables:

- `FLASK_ENV`: Set to `production` for production deployments
- `FLASK_DEBUG`: Set to `false` for production (default)

### Template Customization

Templates can be modified or new ones added in the `Scanner_Nuclei/` directory. Each template follows the standard Nuclei YAML format.

## Error Handling

The API provides comprehensive error handling for:

- **Missing URL Parameter**: Returns 400 with error message
- **Invalid URL Format**: Validates URL structure before scanning
- **Unreachable URLs**: Checks URL accessibility with HEAD requests
- **Invalid JSON**: Handles malformed request bodies

## Security Considerations

- The service validates all input URLs before processing
- ANSI color codes are stripped from output for security
- Subprocess execution is controlled and monitored
- No sensitive information is logged or exposed

## Development

### Local Development

1. Install Python dependencies:
```bash
pip install flask requests
```

2. Install Nuclei:
```bash
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
```

3. Run the application:
```bash
cd Scanner_Nuclei/
python ScanEngine_Nuclei_API.py
```

### Adding New Templates

1. Create a new YAML file in the `Scanner_Nuclei/` directory
2. Follow the Nuclei template format
3. Add the template path to the `templates` list in `ScanEngine_Nuclei_API.py`
4. Test the template with sample targets

## Troubleshooting

### Common Issues

**Service won't start**:
- Check if port 5000 is available
- Verify Docker daemon is running
- Check logs: `docker-compose logs nuclei-scan`

**Scans return no results**:
- Verify target URL is accessible
- Check if templates are properly configured
- Ensure Nuclei binary is installed correctly

**Permission errors**:
- Verify Docker permissions
- Check file permissions in the container

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes and tests
4. Submit a pull request

## License

This project is provided as-is for educational and testing purposes.

## Author

**Mohamed Taha Khattab** - mohamed.taha.khattab0@gmail.com

## Disclaimer

This tool is intended for authorized security testing only. Users are responsible for ensuring they have proper authorization before scanning any targets.
