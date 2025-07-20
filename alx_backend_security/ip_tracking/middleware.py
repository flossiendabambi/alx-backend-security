from django.http import HttpResponseForbidden
from django.core.cache import cache
from ipgeolocation import IpGeolocationAPI
from .models import RequestLog, BlockedIP
from datetime import datetime

API_KEY = 'ed5bdbeb547a481d8c1910ef691d25d6'
geo = IpGeolocationAPI(API_KEY)


class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Block IP
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied: Your IP is blocked.")

        # Get geolocation (cached for 24 hours)
        geo_data = cache.get(ip)
        if not geo_data:
            try:
                response = geo.get_geolocation(ip_address=ip)
                geo_data = {
                    'country': response.get('country_name'),
                    'city': response.get('city')
                }
                cache.set(ip, geo_data, timeout=86400)  # 24 hours
            except Exception:
                geo_data = {'country': None, 'city': None}

        # Save to DB
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            timestamp=datetime.now(),
            country=geo_data.get('country'),
            city=geo_data.get('city')
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
