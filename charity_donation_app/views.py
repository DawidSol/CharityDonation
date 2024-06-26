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
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories,
                                             'institutions': institutions})

    def post(self, request):
        quantity = request.POST.get('bags')
        institution = Institution.objects.get(name=request.POST.get('organization'))
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        phone_number = request.POST.get('phone')
        pick_up_date = request.POST.get('date')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        categories = request.POST.getlist('categories')
        user = request.user
        new_donation = Donation(quantity=quantity, institution=institution,
                                address=address, city=city,
                                zip_code=zip_code, phone_number=phone_number,
                                pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                pick_up_comment=pick_up_comment, user=user)
        new_donation.save()
        new_donation.categories.add(*categories)
        return redirect('form_confirmation')


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
            return redirect('login')


class FormConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UserProfileView(TemplateView):
    template_name = 'user-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        donations = Donation.objects.filter(user=user)
        context['user'] = user
        context['donations'] = donations

        return context
