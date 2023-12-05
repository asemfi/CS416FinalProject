from django.shortcuts import render

# Create your views here.
def view_users(request):
    return render(request, 'users/users.html')


def add_product(request):
    return render(request, 'users/users-form.html')


def update_product(request):
    return render(request, 'users/users-form.html')


def delete_product(request):
    return render(request, 'users/users-form.html')