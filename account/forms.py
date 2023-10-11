from django import forms

from account import models


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码', max_length=32)
    code = forms.CharField(label='验证码', max_length=6)

    class Meta:
        model = models.UserInfo
        fields = "__all__"
        widgets = {
            "password": forms.PasswordInput(),
            "confirm_password": forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = f'请输入{field.label}'
