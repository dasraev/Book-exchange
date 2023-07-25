from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView
from .models import *
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import PasswordResetView
from user.tasks import send_password_reset_email
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404

class RegisterView(CreateView):
    model = MyUser
    template_name = 'user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"{form.cleaned_data['email']} successfully registered")
        return response

    def form_invalid(self, form):
        context = self.get_context_data(form=form, selected_country=form.cleaned_data.get('country'),
                                        selected_region=form.cleaned_data.get('region'))
        return self.render_to_response(context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(self.request, 'user/login.html', {'form': form})

    def post(self, request):
        next_page = self.request.GET.get('next')
        form = LoginForm(self.request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
            if user:
                login(self.request, user)
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('home')
            else:
                messages.error(self.request, "Your username or password didn't match.")

        return render(self.request, 'user/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(self.request)
        messages.success(self.request, 'You are logged out')
        return redirect('login')


class ProfileView(UpdateView):
    model = MyUser
    form_class = ProfileForm
    template_name = 'user/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['countries'] = Country.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profile updated successfully.")
        return response

    def post(self, request, *args, **kwargs):
        print(1111, self.get_object())
        if self.get_object() != request.user:
            raise PermissionDenied()
        return super().post(request, *args, **kwargs)


def regions_by_country(request):
    regions = list(Region.objects.filter(country_id=request.GET.get('country')).values())
    return JsonResponse({"regions": regions})


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            messages.warning(self.request,'There is no such registered user')
            return redirect('password-reset')
        token_generator = default_token_generator
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        reset_link = self.request.build_absolute_uri(
            reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}))
        subject = 'Password reset request'
        message = f'Hi {user.email},\n\nPlease click the link below to reset your password:\n{reset_link}'
        send_password_reset_email.delay(subject, message, email)  # Trigger Celery task
        return redirect('password_reset_done')
