from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Restaurant

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'restaurants', 'birthdate', 'is_active')

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'restaurants', 'birthdate', 'is_active')

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = ('username', 'email', 'role', 'birthdate', 'is_active')
    list_filter = ('role', 'restaurants', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'birthdate')}),
        ('Permissions', {'fields': ('role', 'groups', 'user_permissions', 'is_active')}),
        ('Restaurants', {'fields': ('restaurants',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'restaurants', 'birthdate', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions', 'restaurants')

admin.site.register(User, UserAdmin)

