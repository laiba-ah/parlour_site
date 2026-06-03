from django.contrib import admin
from django.utils.html import format_html

from .models import Booking, TimeSlot, DayOff


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'customer_name',
        'phone',
        'event_type',
        'date',
        'time_slot',
        'status',
        'status_badge',
        'created_at'
    ]

    list_filter = [
        'status',
        'event_type',
        'date'
    ]

    search_fields = [
        'customer_name',
        'phone'
    ]

    date_hierarchy = 'date'
    ordering = ['-date', 'time_slot']

    actions = [
        'mark_confirmed',
        'mark_completed',
        'mark_cancelled'
    ]

    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#198754',
            'completed': '#0d6efd',
            'cancelled': '#dc3545',
            'no_show': '#6c757d',
        }

        color = colors.get(obj.status, '#000')

        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:12px;font-size:12px">{}</span>',
            color,
            obj.get_status_display()
        )

    status_badge.short_description = 'Status Badge'

    @admin.action(description='Mark selected as Confirmed')
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Mark selected as Completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description='Mark selected as Cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['label', 'time', 'is_active']
    list_editable = ['is_active']


@admin.register(DayOff)
class DayOffAdmin(admin.ModelAdmin):
    list_display = ['date', 'reason']