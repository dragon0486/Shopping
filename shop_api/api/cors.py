from django.middleware.security import SecurityMiddleware
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class CORSMiddleware(MiddlewareMixin):
    def process_response(self,request,response):

        response['Access-Control-Allow-Origin'] = "*"

        # 允许你携带Content-Type请求头
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Headers'] = "Content-Type,k1"   # 允许发送数据的请求体类型

        # 允许你发送DELETE,PUT
            response['Access-Control-Allow-Methods'] = "DELETE,PUT"


        return response