import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .helpers import generate_thumbnail, get_thumbnail_url, delete_old_image
from .models import *

# Create your views here.
class RegisterView(View):
    form_class = registerForm
    initial = {'key': 'value'}
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect('/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            username = form.cleaned_data.get('username')
            group, created = Group.objects.get_or_create(name='Users')
            user.groups.add(group)
            messages.success(request, f'Account created for {username}')
            return redirect('account:login')

        return render(request, self.template_name, {'form': form})

# Class based view that extends from the built in login view to add a remember me functionality
class LoginView(LoginView):
    form_class = authenticationForm
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
                
                # Store thumbnail path and username in session
                request.session['user_avatar'] = get_thumbnail_url(user.user_profile)
                request.session['user_username'] = user.username

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
    form_class_user = updateUserForm
    form_class_profile = updateProfileForm
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
            
            # Update session username in case it changed
            request.session['user_username'] = request.user.username

            # Check if a new profile picture is uploaded
            if 'profile_picture' in request.FILES:
                profile.save()
                # Generate thumbnail and update session
                thumb_url = generate_thumbnail(profile)
                request.session['user_avatar'] = thumb_url
                
                # Optional: Delete old image if not default
                if 'default.jpg' not in old_profile_pic:
                    thumbnail_path = os.path.join(os.path.dirname(old_profile_pic), 'thumbs', f"thumb_{os.path.basename(old_profile_pic)}")
                    delete_old_image(old_profile_pic)
                    delete_old_image(thumbnail_path)
            else:
                profile.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('account:users-settings')
        
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})


class DeleteAvatarView(LoginRequiredMixin, View):
    login_url = reverse_lazy('account:login')

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        old_profile_pic = request.user.user_profile.profile_picture.path
        thumbnail_path = os.path.join(os.path.dirname(old_profile_pic), 'thumbs', f"thumb_{os.path.basename(old_profile_pic)}")
        profile.profile_picture = 'Accounts/profile_images/default.jpg'
        delete_old_image(old_profile_pic)
        delete_old_image(thumbnail_path)
        profile.save()
        
        # Reset session avatar to default and ensure username is set
        request.session['user_avatar'] = get_thumbnail_url(profile)
        request.session['user_username'] = request.user.username
        
        messages.success(request, 'Avatar deleted successfully')
        return redirect('account:users-settings')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    login_url = reverse_lazy('account:login')


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('account:login')