
from rest_framework.throttling import SimpleRateThrottle

class SMSRateThrottle(SimpleRateThrottle):
    scope = 'sms'
    def get_cache_key(self, request, view):
        mobile = request.query_params.get('mobile')
        if mobile:
            return 'throttle_%s' % mobile

