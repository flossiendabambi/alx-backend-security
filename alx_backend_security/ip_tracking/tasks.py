from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def detect_anomalies():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    ip_counts = {}
    suspicious_ips = set()

    for log in logs:
        ip = log.ip_address
        ip_counts[ip] = ip_counts.get(ip, 0) + 1

        # Flag if path is sensitive
        if any(log.path.startswith(p) for p in SENSITIVE_PATHS):
            suspicious_ips.add((ip, f"Accessed sensitive path: {log.path}"))

    # Flag IPs with > 100 requests/hour
    for ip, count in ip_counts.items():
        if count > 100:
            suspicious_ips.add((ip, f"{count} requests in the past hour"))

    # Save to SuspiciousIP model
    for ip, reason in suspicious_ips:
        SuspiciousIP.objects.get_or_create(ip_address=ip, reason=reason)
