from django import forms
from django.core.exceptions import ValidationError

from account import models
from account.models import UserInfo
from utils.phone_verification import redis_phone_verification


class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(label='密码', min_length=8, max_length=16, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='确认密码', min_length=8, max_length=16, widget=forms.PasswordInput())
    code = forms.CharField(label='验证码', max_length=6)

    class Meta:
        model = models.UserInfo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = f'请输入{field.label}'

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 5:
            raise ValidationError("用户名长度应为5-10位")
        if UserInfo.objects.filter(username=username).exists():
            raise ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserInfo.objects.filter(email=email).exists():
            raise ValidationError("邮箱已被注册")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if UserInfo.objects.filter(mobile=mobile).exists():
            raise ValidationError("手机号已被注册")
        return mobile

    def clean_code(self):
        mobile = self.cleaned_data.get('mobile', '')
        if not mobile:
            raise ValidationError("验证码错误")
        code = self.cleaned_data['code']
        if not redis_phone_verification.get_verification_code(mobile):
            raise ValidationError("请重新获取验证码")
        if not redis_phone_verification.verify_code(mobile, code):
            raise ValidationError("验证码错误")
        return code

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", '两次密码不一致请重新输入')
