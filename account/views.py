from django.shortcuts import render
from django.views.generic import FormView

from account.forms import RegisterModelForm


# Create your views here.
class Register(FormView):
    form_class = RegisterModelForm
    template_name = "register.html"
