# ALX Backend Security

A Django application for demonstrating backend security mechanisms including IP logging, blacklisting, geolocation analytics, rate limiting, and anomaly detection.

## 🛡️ Features

### ✅ Task 0: Basic IP Logging Middleware
- Logs every incoming request's:
  - IP address
  - Timestamp
  - Path
- Stored in the `RequestLog` model.

### ✅ Task 1: IP Blacklisting
- Middleware blocks requests from blacklisted IPs.
- IPs stored in the `BlockedIP` model.
- Add IPs using a management command:

```bash
python manage.py block_ip <ip_address>
