from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Book, ReservedBook


class UserProfileInline(admin.StackedInline):
    model = UserProfile

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

class BookAdmin(admin.ModelAdmin):
    list_display = ("bname","ISBN","author","genre",)

class ReservedBookAdmin(admin.ModelAdmin):
    list_display = ("user","book","reservation_date",)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(ReservedBook , ReservedBookAdmin)
