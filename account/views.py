import time
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, TemplateView
from django_ratelimit.decorators import ratelimit

from account.forms import RegisterModelForm
from account.models import UserInfo
from account.tasks import send_mail_task
from utils.phone_verification import is_valid, redis_phone_verification
from utils.random_code import get_random_code
from utils.send_sms import send_sms


class Register(FormView):
    form_class = RegisterModelForm
    template_name = "register.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():

            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            mobile = cleaned_data['mobile']
            email = cleaned_data['email']
            cleaned_data.pop('confirm_password', None)
            cleaned_data.pop('code', None)
            user = UserInfo(**cleaned_data)
            send_mail_task.delay(username, mobile, email)

            user.set_password(user.password)
            user.save()
            redis_phone_verification.delete_code(mobile)
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'errors': form.errors})


class SendSms(View):

    @method_decorator(ratelimit(key='ip', rate='1/m', method='POST'))
    @method_decorator(ratelimit(key='ip', rate='10/d', method='POST'))
    @method_decorator(ratelimit(key='post:phone', rate='1/m', method='POST'))
    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone', '')
        tpl = request.POST.get('tpl', '')
        if phone == '':
            return JsonResponse({'status': False, 'error': '手机号不能为空!'})
        elif not is_valid(phone):
            return JsonResponse({'status': False, 'error': '手机格式错误!'})
        elif UserInfo.objects.filter(mobile=phone).exists():
            return JsonResponse({'status': False, 'error': '手机号已被注册!'})
        template_id = settings.TEMPLATE_ID_DICT[tpl]
        code = get_random_code()
        redis_phone_verification.set_verification_code(phone, code)
        send_sms(phone, template_id, code)
        return JsonResponse({'status': True})
        # return JsonResponse({'status': False, 'error': '您的请求过于频繁，请稍后再试!'})


class Login(TemplateView):
    template_name = 'login.html'


def ratelimited_view(request, exception):
    return JsonResponse({'status': False, 'error': '您的请求过于频繁，请稍后再试！'})
