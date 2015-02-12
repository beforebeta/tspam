from django.contrib import admin
from tspam import print_stack_trace
from web.models import *
from django.forms import forms, ModelForm
import requests

class SpamConfigAdminForm(ModelForm):
    class Meta:
        model = SpamConfig

    def clean(self):
        errors = []


        try:
            base_url = self.cleaned_data["website"]
            admin_user = self.cleaned_data["admin_user"]
            admin_password = self.cleaned_data["admin_password"]
            if not ( admin_user and admin_password ):
                errors.append(forms.ValidationError("Base provide an admin user and admin password"))
            if base_url:
                login_url = "https://%s/user/login" % base_url
                s = requests.Session()
                payload = {'return_url': '%s/admin/content/content_list' % base_url,
                           'user_email': admin_user,
                           'user_pass': admin_password}
                response = s.post(login_url, data=payload)
                cookie_data = requests.utils.dict_from_cookiejar(s.cookies)
                if "sdata" not in cookie_data:
                    errors.append(forms.ValidationError("Invalid admin user or password"))
            else:
                errors.append(forms.ValidationError("Base provide a Base URL"))
        except:
            print_stack_trace()




        try:
            stop_words = get_stopwords()
            title_scan_spam_filter_fields = self.cleaned_data["title_scan_spam_filter_fields"]
            if title_scan_spam_filter_fields:
                title_scan_spam_filter_fields = [f.lower().strip() for f in title_scan_spam_filter_fields.split("\n") if f.lower().strip()]
            content_scan_spam_filter_fields = self.cleaned_data["content_scan_spam_filter_fields"]
            if content_scan_spam_filter_fields:
                content_scan_spam_filter_fields = [f.lower().strip() for f in content_scan_spam_filter_fields.split("\n") if f.lower().strip()]
            fields = []
            fields.extend(title_scan_spam_filter_fields)
            fields.extend(content_scan_spam_filter_fields)
            for f in fields:
                if f in stop_words:
                    errors.append(forms.ValidationError("Term '%s' is not allowed because its too common" % f))
        except:
            print_stack_trace()
            raise forms.ValidationError("An error occurred when saving the data")
        if errors:
            raise forms.ValidationError(errors)
        else:
            return self.cleaned_data


class SpamConfigAdmin(admin.ModelAdmin):
    readonly_fields = ('last_complete_run','created', 'modified',)
    form = SpamConfigAdminForm


def ignore_spam(modeladmin, request, queryset):
    for spam_post in queryset:
        if spam_post.status == "identified":
            spam_post.ignore()

ignore_spam.short_description = "Not Spam, Ignore This Post"

def delete_spam(modeladmin, request, queryset):
    session_per_config = {}
    for spam_post in queryset:
        if spam_post.status != "deleted":
            if spam_post.config_id not in session_per_config:
                session_per_config[spam_post.config_id] = login("https://%s" % spam_post.config.website, spam_post.config)
            spam_post.delete_spam(authenticated_session=session_per_config[spam_post.config_id])

delete_spam.short_description = "Confirm as Spam and Delete from Website"

class SpamPostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified',)
    list_display = ('config', 'post_id', 'post_title', "post_user", "title_scan_hits", "content_scan_hits", "status")
    search_fields = ["config__website", 'post_id', 'post_title', "title_scan_hits", "content_scan_hits", "post_user"]
    actions = [delete_spam, ignore_spam]

admin.site.register(SpamConfig, SpamConfigAdmin)

admin.site.register(SystemConfig)


class SpamScanAdmin(admin.ModelAdmin):
    list_display = ('config', 'started', "ended")

admin.site.register(SpamScan, SpamScanAdmin)
admin.site.register(SpamPost, SpamPostAdmin)

