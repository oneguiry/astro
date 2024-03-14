from django.contrib import admin

from core.models import AccountManager


@admin.register(AccountManager)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'user_email')

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'

