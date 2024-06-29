import datetime

from django.contrib import admin
from django.db.models import Q

from schedule.forms import EventAdminForm
from schedule.models import (
    Calendar,
    Event,
)


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    fieldsets = ((None, {"fields": [("name", "slug")]}),)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "formatted_start", "formatted_end")
    list_filter = ("start", "calendar",)
    ordering = ("-start",)
    date_hierarchy = "start"
    search_fields = ("title", "description")
    fieldsets = (
        (
            None,
            {
                "fields": [
                    ("title", "color_event"),
                    ("description",),
                    ("start", "end"),
                    ("creator", "calendar"),
                    ("rule", "end_recurring_period"),
                ]
            },
        ),
    )
    form = EventAdminForm
    actions = ('duplicate_event_5', 'duplicate_event_10',)

    def _duplicate_event(self, request, queryset, count):
        for curr_event in queryset:
            first_event = curr_event
            for _ in range(count):
                event = Event(
                    title=first_event.title,
                    description=first_event.description,
                    start=first_event.start + datetime.timedelta(days=1),
                    end=first_event.end + datetime.timedelta(days=1),
                    calendar=first_event.calendar,
                    )
                exists = Event.objects.filter(
                    Q(title=first_event.title) &
                    Q(description=first_event.description) &
                    Q(start=first_event.start + datetime.timedelta(days=1)) &
                    Q(end=first_event.end + datetime.timedelta(days=1)) &
                    Q(calendar=first_event.calendar)
                    )
                if not exists:
                    event.save()
                first_event = event

    def duplicate_event_5(self, request, queryset):
        self._duplicate_event(request, queryset, 5)
        
    duplicate_event_5.short_description = "Создать копии (5)"

    def duplicate_event_10(self, request, queryset):
        self._duplicate_event(request, queryset, 10)

    duplicate_event_10.short_description = "Создать копии (10)"

    def formatted_start(self, obj):
        return obj.start.strftime('%d %B %Y %H:%M')
    formatted_start.admin_order_field = 'start'
    formatted_start.short_description = 'Start Date and Time'

    def formatted_end(self, obj):
        return obj.end.strftime('%d %B %Y %H:%M')
    formatted_end.admin_order_field = 'end'
    formatted_end.short_description = 'End Date and Time'

