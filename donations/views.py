from django.shortcuts import render
from django.views import View
from django.db.models import Sum

from donations.models import Donation


class LandingPage(View):

    @staticmethod
    def count_bags():
        bags_count = Donation.objects.aggregate(Sum('quantity'))
        return bags_count['quantity__sum']

    @staticmethod
    def count_supported_institutions():
        institutions_count = Donation.objects.distinct('institution').count()
        return institutions_count

    def get(self, request):
        context = {}
        context['bags_count'] = self.count_bags()
        context['supported_institutions_count'] = self.count_supported_institutions()

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
