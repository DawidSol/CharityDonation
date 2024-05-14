import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from charity_donation_app.models import Donation, Institution, Category


class LandingPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        donations = Donation.objects.all()
        foundations = Institution.objects.filter(type=0)
        organizations = Institution.objects.filter(type=1)
        collections = Institution.objects.filter(type=2)
        bags_donated = sum(donation.quantity for donation in donations)
        institutions_helped = sum(len(institution) for institution in [foundations, organizations, collections])

        context['foundations'] = foundations
        context['organizations'] = organizations
        context['collections'] = collections
        context['bags_donated'] = bags_donated
        context['institutions_helped'] = institutions_helped

        return context


class AddDonationView(View):

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'form.html', {'categories': categories})


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Nie ma takiego użytkownika.')
            return redirect('register')
        else:
            login(request, user)
            messages.success(request, 'Zalogowano.')
            return redirect('landing')


class LogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, 'Wylogowano.')
        return redirect('landing')


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        try:
            user = User.objects.get(email=email)
            if user is not None:
                messages.error(request, 'Użytkownik już istnieje.')
                return render(request, 'register.html')
        except User.DoesNotExist:

            if not all([name, surname, email, password, password2]):
                messages.error(request, "Wszystkie pola formularza muszą być wypełnione.")
                return render(request, 'register.html')

            if password != password2:
                messages.error(request, "Hasła nie są identyczne.")
                return render(request, 'register.html')

            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                messages.error(request, "Nieprawidłowy adres email.")
                return render(request, 'register.html')

            if not (all(char.isalpha() or char.isspace() or char == '-' for char in name) and
                    all(char.isalpha() or char.isspace() or char == '-' for char in surname)):
                messages.error(request, "Imię i nazwisko nie mogą zawierać znaków specjalnych.")
                return render(request, 'register.html')

            User.objects.create_user(username=email, first_name=name, last_name=surname, email=email, password=password)
            return render(request, 'login.html')
