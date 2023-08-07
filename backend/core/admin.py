from django.contrib import admin
from django import forms
from django.template.response import TemplateResponse
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib import messages

from guardian.admin import GuardedModelAdmin
from adminsortable2.admin import SortableInlineAdminMixin

from . import models


class UserSetForm(forms.ModelForm):
    active = forms.BooleanField(required=False)

    class Meta:
        model = models.User.groups.through
        fields = ["user", "active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["active"].initial = self.instance.user.active


class UserSetFormSet(forms.BaseInlineFormSet):
    def save_existing(self, form, instance, commit=True):
        instance.user.active = form.cleaned_data.get("active")
        instance.user.save()
        return super().save_existing(form, instance, commit)


class UserSetInline(admin.TabularInline):
    model = models.User.groups.through
    raw_id_fields = ("user",)
    form = UserSetForm
    formset = UserSetFormSet


@admin.register(models.Team)
class TeamAdmin(GuardedModelAdmin):
    list_display = ["name", "active"]
    list_filter = ["active"]
    search_fields = ["name"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "active",
                    "sponsor_organisation",
                    "school_organisation",
                    # "created_date",
                )
            },
        ),
    )
    inlines = [UserSetInline]
    actions = ['deactivate_team_members', 'bulk_regenerate_cards_for_members']
    ordering = ["name"]
    
    def deactivate_team_members(self, request, queryset: object):
        for team in queryset:
            for team_member in team.active_users:
                team_member.active = False
                team_member.save()

    def bulk_regenerate_cards_for_members(self, request, queryset: object):
        if request.POST.get('post', None):
            from long_running_request_actors import bulk_regenerate_cards_for_team as actor
          
            for team in queryset:
                resp = actor.send_with_options(kwargs={"team_id": team.pk})
            messages.add_message(request, messages.INFO, f"Regenerating cards in the background")

        else:
            opts = self.model._meta
            request.current_app = self.admin_site.name
            
            return TemplateResponse(request, "admin/bulk_regenerate_cards_for_members_confirm.html", {
                "opts": opts,
                "app_label": opts.app_label,
                "queryset": queryset,
                "action_checkbox_name": ACTION_CHECKBOX_NAME
            })
        

admin.site.register(models.UserProfile)


class StreamCurriculumInline(
    SortableInlineAdminMixin, admin.TabularInline
):  # or admin.StackedInline
    model = models.StreamCurriculum


@admin.register(models.Stream)
class StreamAdmin(admin.ModelAdmin):
    inlines = (StreamCurriculumInline,)
    ordering = ["name"]


@admin.register(models.StreamRegistration)
class StreamRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "name",
        "start_date",
        "latest_end_date",
        "ideal_end_date",
        "active",
    ]
    list_filter = ["active", "stream", "employer_partner"]
    search_fields = ["name", "user__email"]


admin.site.site_header = "Tilde Administration"
admin.site.enable_nav_sidebar = False
