from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib import messages
from accounts.forms import SignUpForm, EditUserForm
from django.contrib.auth.models import User
from ticketMaster.views import is_saved
from ticketMaster.models import Event, Comment, SavedEvent


# Rana Naimat
# Create your views here.
@login_required(login_url='login')
def index(request):
    context = {'savedEvents': get_saved_events(request.user)}  # savedEvents is an array of dictionaries}
    return render(request, 'accounts/index.html', context)


def update_view(request):
    user = request.user
    user_object = User.objects.get(id=user.id)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user_object)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = EditUserForm(instance=user_object)

    context = {'form': form}
    return render(request, 'accounts/update.html', context)


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

    context = {
        'form': form
    }

    return render(request, 'accounts/login.html', context)


def get_saved_events(current_user):
    saved_events = SavedEvent.objects.filter(user=current_user)

    return_events = []

    for saved_event in saved_events:
        # get event, log details
        event = saved_event.eventID
        event_details = {
            'event_id': event.event_id,
            'eventName': event.eventName,
            'eventLink': event.eventLink,
            'imageLink': event.imageLink,
            'venue': event.venue,
            'localDate': event.localDate,
            'localTime': event.localTime,
            'address': event.address,
            'cityState': event.cityState,
            'googleMap': event.googleMap,
        }

        return_events.append(event_details)

    return return_events


def logout_view(request):
    messages.info(request, 'You are Logged out')
    logout(request)
    return redirect('index')


class PasswordContexMixin:
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


class PasswordResetView(PasswordContexMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    from_class = PasswordResetForm
    from_email = 'ticketmasterapi@outlook.com'
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
