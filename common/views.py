from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm


# Create your views here.
def signup(request):
    if request.method == "POST":
        return signup_post(request)
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


def signup_post(request):
    form = UserForm(request.POST)
    if not form.is_valid():
        return render(request, 'common/signup.html', {'form': form})
    form.save()
    username = form.cleaned_data.get('username')
    raw_password = form.cleaned_data.get('password1')
    user = authenticate(username=username, password=raw_password)
    login(request, user)
    return redirect('index')


