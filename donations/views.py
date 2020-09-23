from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, password_changed
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.core.validators import validate_email, MinLengthValidator
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.db.models import Sum
from django.views.generic import FormView, UpdateView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from donations.forms import RegisterForm, UserProfileEditForm
from donations.models import Donation, Institution, Category
from donations.serializers import DonationSerializer, UserProfileSerializer, UserPasswordSerializer


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


class AddDonation(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'categories': Category.objects.all(),
            'institutions': Institution.objects.all()
        }
        return render(request, 'form.html', context)

    def post(self, request):
        quantity = int(request.POST.get('bags'))
        categories = request.POST.getlist('categories')
        institution = Institution.objects.get(id=int(request.POST.get('institution')))
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        phone_number = request.POST.get('phone')
        pick_up_date = request.POST.get('date')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = request.user

        donation = Donation(
            quantity=quantity,
            institution=institution,
            address=address,
            city=city,
            zip_code=zip_code,
            phone_number=phone_number,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user
        )
        try:
            donation.save()

            for category in categories:
                donation.categories.add(category)

            return render(request, 'form-confirmation.html')
        except Exception as ex:
            print(ex)
            return render(request, 'form-confirmation.html')


class Login(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect(reverse('landing_page'))
        else:
            return redirect(reverse('register') + '#register')


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('landing_page'))


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


class UserProfile(LoginRequiredMixin, View):

    def get(self, request):
        donations = request.user.donation_set.all().order_by('-pick_up_date').order_by('-pick_up_time')
        pending_donations = donations.filter(is_taken=False)
        archived_donations = donations.filter(is_taken=True)
        context = {
            'user_donations': pending_donations,
            'archived_user_donations': archived_donations,
        }
        return render(request, 'user_profile.html', context)


class DonationUpdate(UpdateAPIView):
    queryset = Donation.objects.all()
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = DonationSerializer


class UserProfileEdit(LoginRequiredMixin, FormView):
    form_class = UserProfileEditForm
    template_name = 'user_profile_edit.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form: ModelForm
        user = self.request.user
        form = super().get_form(form_class)
        form.fields['username'].help_text = ''
        form.fields['username'].initial = user.username
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        return form


class UserProfileUpdate(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        if check_password(request.data['password'], self.request.user.password):
            return super().update(request, args, kwargs)
        else:
            return Response(status=500)


class UserPasswordUpdate(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = UserPasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer: Serializer
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                validate_password(serializer.data.get('new_password1'))
                validate_password(serializer.data.get('new_password2'))
            except ValidationError:
                return Response(status=500)

            if not check_password(serializer.data.get('old_password'), self.request.user.password):
                return Response(status=500)

            user.set_password(serializer.data.get('new_password2'))
            user.save()
            login(request, user)

            return Response({
                'status': 'success',
                'code': 200
            })
        else:
            return Response(status=500)
