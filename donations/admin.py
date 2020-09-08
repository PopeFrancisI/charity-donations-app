from django.contrib import admin
from donations.models import Donation, Institution, Category

admin.site.register(Donation)
admin.site.register(Institution)
admin.site.register(Category)