from django.shortcuts import render
from django.views import View

from donations.models import Donation


class LandingPage(View):

    @staticmethod
    def count_bags():
        bags_count = Donation.objects.all().aggregate(sum('quantity'))
        return bags_count

    def get(self, request):
        context = {}
        context['bags_count'] = self.count_bags()
        context['supported_organisations_count'] = count_supported_organisations()

        return render(request, 'index.html', context)


class AddDonation(View):

    def get(self, request):
        return render(request, 'form.html')


class Login(View):

    def get(self, request):
        return render(request, 'login.html')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')
