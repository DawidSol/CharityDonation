from django.shortcuts import render
from django.views import View
from charity_donation_app.models import Donation, Institution


class LandingPageView(View):

    def get(self, request):
        donations = Donation.objects.all()
        institutions = Institution.objects.all()
        bags_donated = sum(donation.quantity for donation in donations)
        institutions_helped = len(institutions)
        return render(request, 'index.html', {'bags_donated': bags_donated,
                                              'institutions_helped': institutions_helped, 'institutions': institutions})


class AddDonationView(View):

    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')
