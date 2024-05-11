import re
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import render
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
                return HttpResponseBadRequest("Użytkownik już istnieje")
        except User.DoesNotExist:

            if not all([name, surname, email, password, password2]):
                return HttpResponseBadRequest("Wszystkie pola formularza muszą być wypełnione.")

            if password != password2:
                return HttpResponseBadRequest("Hasła nie są identyczne.")

            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                return HttpResponseBadRequest("Nieprawidłowy adres email.")

            if not (all(char.isalpha() or char.isspace() or char == '-' for char in name) and
                    all(char.isalpha() or char.isspace() or char == '-' for char in surname)):
                return HttpResponseBadRequest("Imię i nazwisko nie mogą zawierać znaków specjalnych.")

            User.objects.create_user(username=email, first_name=name, last_name=surname, email=email, password=password)
            return render(request, 'login.html')
