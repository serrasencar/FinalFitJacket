from django.contrib import admin
from .models import Badge, UserBadge


class UserBadgeInline(admin.TabularInline):
    model = UserBadge
    extra = 1  # Number of extra forms to show


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rule_type', 'threshold')
    list_filter = ('rule_type',)
    search_fields = ('name', 'rule_type')
    inlines = [UserBadgeInline]


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')
    list_filter = ('badge__name',)
    search_fields = ('user__username', 'badge__name')
    readonly_fields = ('awarded_at',)
