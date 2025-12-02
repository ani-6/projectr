import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
#from .helpers import generate_thumbnail, delete_old_image
from .models import *

# Create your views here.
class registerView(View):
    form_class = register_form
    initial = {'key': 'value'}
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(registerView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Users')   #Get users group
            user.groups.add(group)     #Add user to users group
            messages.success(request, f'Account created for {username}')
            return redirect(to='account:login')

        return render(request, self.template_name, {'form': form})

# Class based view that extends from the built in login view to add a remember me functionality
class customLoginView(LoginView):
    form_class = customAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Try to authenticate using email
            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                # Try to authenticate using username
                user = authenticate(request, email=username_or_email, password=password)

            if user is not None:
                login(request, user)
                remember_me = form.cleaned_data.get('remember_me')
                if not remember_me:
                    request.session.set_expiry(600)
                    request.session.modified = True
                else:
                    request.session['remember_me'] = True
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

class resetPassword(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('account:login')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('account:users-settings')


class SettingsView(LoginRequiredMixin, View):
    form_class_user = updateUser_form
    form_class_profile = updateProfile_form
    template_name = 'accounts/settings.html'
    login_url = reverse_lazy('account:login')

    def get(self, request, *args, **kwargs):
        user_form = self.form_class_user(instance=request.user)
        profile_form = self.form_class_profile(instance=request.user.user_profile)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        old_profile_pic = request.user.user_profile.profile_picture.path
        user_form = self.form_class_user(request.POST, instance=request.user)
        profile_form = self.form_class_profile(request.POST, request.FILES, instance=request.user.user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            # Check if a new profile picture is uploaded
            if 'profile_picture' in request.FILES:
                profile.save()
                # Generate thumbnail
                #generate_thumbnail(profile.profile_picture.path)
                #delete_old_image(old_profile_pic)
            else:
                profile.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='account:users-settings')
        
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})


class DeleteAvatarView(LoginRequiredMixin, View):
    login_url = reverse_lazy('account:login')

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        old_profile_pic = request.user.user_profile.profile_picture.path
        profile.profile_picture = 'Accounts/profile_images/default.jpg'
        #delete_old_image(old_profile_pic)
        profile.save()
        messages.success(request, 'Avatar deleted successfully')
        return redirect(to='account:users-settings')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = reverse_lazy('account:login')


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('account:login')
