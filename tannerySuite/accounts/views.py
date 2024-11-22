from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm
from .forms import FormRegistrazione



def registrazione_view(request):
    if request.method == 'POST':
        form = FormRegistrazione(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            user = authenticate(username=username, password=password,)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = FormRegistrazione()
    context = {"form": form}
    return render(request, "accounts/registrazione.html", context)
        

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                request.FILES,
                                instance=request.user.profile
                                )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'accounts/profile.html', context)
# @login_required
# def profile(request):
#     return render(request, 'profile.html')