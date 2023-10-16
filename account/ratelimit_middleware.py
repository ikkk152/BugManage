from django.http import JsonResponse


# 弃用,使用现成中间件RateLimitMiddleware
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 检查是否由 django_ratelimit 设置的属性
        if getattr(request, 'limited', False):
            return JsonResponse({'status': False, 'error': '您的请求过于频繁，请稍后再试！'})

        return response
