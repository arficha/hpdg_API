from django.contrib import admin
from .models import *

admin.site.register(Token)
admin.site.register(Client)
admin.site.register(Admin)
admin.site.register(Superadmin)
admin.site.register(Entite)
admin.site.register(Reservation)
admin.site.register(Chambre)
admin.site.register(Photo)

# Register your models here.
