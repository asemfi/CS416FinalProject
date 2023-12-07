from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib import messages
from accounts.forms import SignUpForm
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request, 'accounts/index.html')


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def delete_user(request):
    user = User.objects.get(user=request.user)
    user.delete()
    return redirect('index')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')

    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    messages.info(request, 'You are Logged out')
    logout(request)
    return redirect('index')


class PasswordConteexMixin:
    extra_context = None

    def __init__(self):
        self.title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(self, **kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordResetView(PasswordConteexMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    from_class = PasswordResetForm
    from_email = ''
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
