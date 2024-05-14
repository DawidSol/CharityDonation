from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View


class LandingPageView(View):

    def get(self, request):
        return render(request, 'index.html')


class AddDonationView(View):

    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return redirect('register')
        else:
            login(request, user)
            return redirect('landing')


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('landing')


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')
