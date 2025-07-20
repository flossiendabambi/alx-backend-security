from django.shortcuts import render
from django.http import JsonResponse
from ratelimit.decorators import ratelimit

# For anonymous users (5/minute)
@ratelimit(key='ip', rate='5/m', block=True)
def anonymous_sensitive_view(request):
    return JsonResponse({"message": "Anonymous request successful!"})

# For authenticated users (10/minute)
@ratelimit(key='ip', rate='10/m', block=True)
def authenticated_sensitive_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    return JsonResponse({"message": "Authenticated request successful!"})

