from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from charity_donation_app.models import Donation, Institution


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
        return render(request, 'form.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')
