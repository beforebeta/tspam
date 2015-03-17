from django.db import models
from django.utils.timezone import now
from tspam import print_stack_trace
from bs4 import BeautifulSoup
import requests
from web import send_email


class Timestamps(models.Model):
    created = models.DateTimeField(blank=True)
    modified = models.DateTimeField(blank=True)

    def save(self, *args, **kw):
        if not self.id:
            if not self.created:
                self.created = now()
        self.modified = now()
        super(Timestamps, self).save(*args, **kw)

    class Meta:
        abstract = True

class SpamConfig(Timestamps):
    website = models.CharField(max_length=255, null=True, blank=True, help_text="Expected format is www.website_name.com. Example: www.finehomebuilding.com")
    title_scan_spam_filter_fields = models.TextField(null=True, blank=True, help_text="Use this section to specify the terms that should be checked in the title of the posting. If a posting's title contains any of the terms in this list, it will be deleted.")
    content_scan_spam_filter_fields = models.TextField(null=True, blank=True, help_text="Use this section to specify the terms that should be checked in the body of the posting. Be VERY CAREFUL with the terms you enter here. If a posting's content contains any of the terms in this list, it will be deleted. When in doubt, ignore this section.")
    last_complete_run = models.DateTimeField(null=True, blank=True)
    spam_user_names = models.TextField(null=True, blank=True)
    is_full_scan_needed = models.BooleanField(default=False, help_text="Should the scanner review the latest 20 pages of posts or should it do an entire scan of the site?")
    deactivate_spam_user = models.BooleanField(default=False, help_text="If a post is identified as SPAM, should the corresponding user be deactivated (status=0)?")
    notification_recipients = models.TextField(null=True, blank=True, help_text="Enter your email address here if you wish to be notified when new spam is found")
    admin_user = models.CharField(max_length=255, null=True)
    admin_password = models.CharField(max_length=255, null=True)

    def save(self, *args, **kw):
        if not self.id:
            if not self.created:
                self.created = now()
        if self.title_scan_spam_filter_fields:
            self.title_scan_spam_filter_fields = "\n".join([f.lower().strip() for f in self.title_scan_spam_filter_fields.split("\n") if f.lower().strip()])
        if self.content_scan_spam_filter_fields:
            self.content_scan_spam_filter_fields = "\n".join([f.lower().strip() for f in self.content_scan_spam_filter_fields.split("\n") if f.lower().strip()])
        if self.spam_user_names:
            self.spam_user_names = "\n".join([f.lower().strip() for f in self.spam_user_names.split("\n") if f.lower().strip()])
        self.modified = now()
        super(SpamConfig, self).save(*args, **kw)

    def get_title_scan_list(self):
        return [f.lower().strip() for f in self.title_scan_spam_filter_fields.split("\n") if f.lower().strip()]

    def get_content_scan_list(self):
        return [f.lower().strip() for f in self.content_scan_spam_filter_fields.split("\n") if f.lower().strip()]

    def __unicode__(self):
        return "%s" % self.website

    def deactivate_spam_user_action(self, auth_session, post_user_edit, post_user):
        payload={"user_status":0, "editmode":"status"}
        url = "https://%s%s" % (self.website, post_user_edit)
        auth_session.post(url, data=payload)
        try:
            user_names_set = "\n".join([x.lower().strip() for x in set(self.spam_user_names.split("\n") + SpamConfig.objects.get(id=self.id).spam_user_names.split("\n") + [post_user.lower()]) if x])
            SpamConfig.objects.filter(id=self.id).update(spam_user_names=user_names_set)
        except:
            print_stack_trace()

def login(base_url, config):
    """
    returns the session if the user can successfully authenticate, otherwise returns None
    """
    login_url = "%s/user/login" % base_url
    s = requests.Session()
    payload = {'return_url': '%s/admin/content/content_list' % base_url,
               'user_email': config.admin_user,
               'user_pass': config.admin_password}
    response = s.post(login_url, data=payload)
    cookie_data = requests.utils.dict_from_cookiejar(s.cookies)
    if "sdata" in cookie_data:
        return s
    else:
        return None

class SystemConfig(Timestamps):
    stopwords_list = models.TextField(null=True, blank=True)

def get_stopwords():
    words = []
    try:
        for s in SystemConfig.objects.all()[0].stopwords_list.split("\n"):
            words.append(s.lower().strip())
    except:
        print_stack_trace()
    return words

class SpamScan(Timestamps):
    config = models.ForeignKey(SpamConfig)
    website = models.CharField(max_length=255, null=True, blank=True)
    started = models.DateTimeField(null=True, blank=True)
    ended = models.DateTimeField(null=True, blank=True)
    log = models.TextField(blank=True, null=True)

    def start(self, spam_config):
        self.config = spam_config
        self.started = now()
        self.log = "Started: %s" % self.started.strftime("%c")
        self.save()

    def end(self):
        self.ended = now()
        self.config.last_complete_run = self.ended
        self.config.save()
        self.save()
        self.add_log("Ended: %s" % self.ended.strftime("%c"))
        # try:
        #     send_email(
        #
        #     )
        # except:
        #     print_stack_trace()

    def save(self, *args, **kw):
        if self.config:
            self.website = self.config.website
        super(SpamScan, self).save(*args, **kw)

    def add_log(self, log_item):
        print log_item
        self.log = "%s\n%s" % (self.log, log_item)
        self.save()


class SpamPost(Timestamps):
    config = models.ForeignKey(SpamConfig)
    post_id = models.CharField(max_length=255, null=True, blank=True)
    post_title = models.CharField(max_length=255, null=True, blank=True)
    post_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="identified") #identified, deleted
    post_user = models.CharField(max_length=255, null=True, blank=True)
    post_user_edit = models.CharField(max_length=255, null=True, blank=True)

    title_scan_hits = models.TextField(blank=True, null=True)
    content_scan_hits = models.TextField(blank=True, null=True)

    def save(self, *args, **kw):
        if self.config:
            try:
                if self.post_title:
                    self.title_scan_hits = "\n".join([x for x in self.config.get_title_scan_list() if x in self.post_title.lower()])
            except:
                # print_stack_trace()
                pass
            try:
                if self.post_text:
                    soup = BeautifulSoup(self.post_text)
                    body = soup.find("div", {"id": "left"})
                self.content_scan_hits = "\n".join([x for x in self.config.get_content_scan_list() if x in body.text.lower()])
            except:
                pass
                # print_stack_trace()
        super(SpamPost, self).save(*args, **kw)

    def ignore(self):
        self.status = "ignored"
        self.save()

    def delete_spam(self, authenticated_session=None):
        auth_session = authenticated_session
        if not auth_session:
            auth_session = login("https://%s" % self.config.website, self.config)
        if self.config.deactivate_spam_user:
            self.config.deactivate_spam_user_action(auth_session, self.post_user_edit, self.post_user)
        payload={"delete":1}
        delete_url = "https://%s/share/delete/%s" % (self.config.website, self.post_id)
        try:
            response = auth_session.post(delete_url, data=payload)
            if response.status_code == 200:
                self.status = "deleted"
            else:
                self.status = "error"
        except:
            print_stack_trace()
            self.status = "error"
        self.save()