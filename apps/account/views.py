from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .forms import *
from .helpers import generate_thumbnail, get_thumbnail_url, delete_old_image
from .models import *

# ... (Previous Views: RegisterView, LoginView) ...
# Ensure RegisterView and LoginView code remains here as previously defined
class RegisterView(View):
    form_class = registerForm
    initial = {'key': 'value'}
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
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

class LoginView(LoginView):
    form_class = authenticationForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if hasattr(user, 'user_profile'):
             self.request.session['user_avatar'] = get_thumbnail_url(user.user_profile)
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(600)
            self.request.session.modified = True
        else:
            self.request.session['remember_me'] = True
        return HttpResponseRedirect(self.get_success_url())

class resetPassword(SuccessMessageMixin, PasswordResetView):
    form_class = CustomPasswordResetForm 
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password."
    success_url = reverse_lazy('account:login')

# --- Updated Change Password View ---
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm # Use the new styled form
    template_name = 'account/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('account:users-settings')

class SettingsView(LoginRequiredMixin, View):
    form_class_user = updateUserForm
    form_class_profile = updateProfileForm
    template_name = 'account/settings.html'
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
            request.session['user_username'] = request.user.username
            if 'profile_picture' in request.FILES:
                profile.save()
                thumb_url = generate_thumbnail(profile)
                request.session['user_avatar'] = thumb_url
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
        profile.profile_picture = 'Account/profile_images/default.jpg'
        delete_old_image(old_profile_pic)
        delete_old_image(thumbnail_path)
        profile.save()
        request.session['user_avatar'] = get_thumbnail_url(profile)
        messages.success(request, 'Avatar deleted successfully')
        return redirect('account:users-settings')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'
    login_url = reverse_lazy('account:login')

class LogoutUserView(LogoutView):
    next_page = reverse_lazy('account:login')