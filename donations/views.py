from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.db.models import Sum
from django.views.generic import FormView

from donations.forms import RegisterForm
from donations.models import Donation, Institution


class LandingPage(View):

    @staticmethod
    def count_bags():
        bags_count = Donation.objects.aggregate(Sum('quantity'))
        return bags_count['quantity__sum']

    @staticmethod
    def count_supported_institutions():
        institutions_count = Donation.objects.distinct('institution').count()
        return institutions_count

    @staticmethod
    def get_institutions_of_type(type):
        institutions = Institution.objects.filter(type=type)
        return institutions

    def get_page_obj(self, queryset, page_name, per_page_count=1):
        paginator = Paginator(queryset, per_page_count)
        page_number = self.request.GET.get(page_name)
        page_obj = paginator.get_page(page_number)
        return page_obj

    def get(self, request):
        context = {}
        context['bags_count'] = self.count_bags()
        context['supported_institutions_count'] = self.count_supported_institutions()

        charities_page_name = 'charities_page'
        ngos_page_name = 'ngos_page'
        local_collections_page_name = 'local_collections_page'

        charities = self.get_institutions_of_type('C')
        charities_page = self.get_page_obj(charities, charities_page_name)
        context[charities_page_name] = charities_page
        context['charities_page_range'] = range(1, charities_page.paginator.num_pages + 1)

        ngos = self.get_institutions_of_type('NGO')
        ngos_page = self.get_page_obj(ngos, ngos_page_name)
        context[ngos_page_name] = ngos_page
        context['ngos_page_range'] = range(1, ngos_page.paginator.num_pages + 1)

        local_collections = self.get_institutions_of_type('L')
        local_collections_page = self.get_page_obj(local_collections, local_collections_page_name)
        context[local_collections_page_name] = local_collections_page
        context['local_collections_page_range'] = range(1, local_collections_page.paginator.num_pages + 1)

        return render(request, 'index.html', context)


class AddDonation(View):

    def get(self, request):
        return render(request, 'form.html')


class Login(View):

    def get(self, request):
        return render(request, 'login.html')


class Register(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        new_user = User(
            username=email,
            first_name=first_name,
            last_name=last_name
        )
        new_user.set_password(password)
        new_user.save()

        return redirect(f'{self.get_success_url()}#login')
