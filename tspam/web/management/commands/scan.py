from optparse import make_option
from django.core.management.base import BaseCommand
import requests
from web.models import SpamScan, SpamConfig, SpamPost
from bs4 import BeautifulSoup
from django.utils.text import compress_string
import traceback
import math
def get_stack_trace():
    return traceback.format_exc()

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--run', action='store_true', dest='run', default=False, help='run'),)

    def handle(self, *args, **options):
        if options['run']:
            run()

def _login(base_url, config):
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

def _get_num_pages(base_url, config, auth_session):
    pages = 1
    response = auth_session.get("%s/admin/content/content_list/sort/post_modified/page/1?sort_field=post_modified&sort_order=DESC" % base_url)
    soup = BeautifulSoup(response.content)
    div = None
    try:
        div = soup.find_all("div", class_="viewing")[0]
    except:
        div = soup.find_all("ul", class_="pagination")[0].parent
    line = div.text.strip().split("\n")[0]
    pages = int(line[line.index("of")+3:line.index("posts")-1])
    return int(math.ceil(float(pages)/20))

def _scan_page(page, base_url, config, auth_session, title_scan_list, content_scan_list, scan):
    response = auth_session.get("%s/admin/content/content_list/sort/post_modified/page/%s?sort_field=post_modified&sort_order=DESC" % (base_url, page))
    soup = BeautifulSoup(response.content)
    posts = soup.find_all("tr", class_="bg-grey")
    posts.extend(soup.find_all("tr", class_="bg-white"))

    if not posts:
        posts = soup.find_all("table", class_="admin-list")[0].find_all("tr")[1:]

    def _identify_post_for_deletion(tds):
        post = SpamPost()
        post.config = config
        post.post_id = tds[1].text.lower().strip()
        post.post_title = tds[4].text.lower().strip()
        try:
            post.post_text = auth_session.get("%s/item/%s" % (base_url, post.post_id)).content
        except:
            post.post_text = ""
        post.status = "identified"
        post.post_user = tds[7].text.lower().strip()
        post.post_user_edit = tds[7].find_all("a")[0]["href"]
        if SpamPost.objects.filter(post_id=post.post_id).count() == 0:
            try:
                post.save()
            except:
                post.post_text = ""
                post.save()
            scan.add_log("identified %s for deletion" % tds[1].text)

    for post in posts:
        try:
            tds = post.find_all("td")
            if len(tds) <= 6:
                continue
            if any(x in tds[4].text.lower() for x in title_scan_list):
                _identify_post_for_deletion(tds)
            else:
                response = auth_session.get("%s/item/%s" % (base_url, tds[1].text.lower().strip()))
                soup = BeautifulSoup(response.content)
                body = soup.find("div", {"id": "left"})
                try:
                    if any(x in body.text.lower() for x in content_scan_list):
                        _identify_post_for_deletion(tds)
                except:
                    pass
        except:
            st = get_stack_trace()
            scan.add_log(st)

def run():
    for config in SpamConfig.objects.all():
        # if "woodwo" not in config.website:
        #     continue
        print config.website
        if not config.get_title_scan_list() and not config.get_content_scan_list():
            print "skipping because nothing to scan"
            continue
        scan = SpamScan()
        scan.start(config)
        try:
            base_url = "https://%s" % config.website
            auth_session = _login(base_url, config)
            if not auth_session:
                scan.add_log("Error: could not log in")
            else:
                title_scan_list = config.get_title_scan_list()
                content_scan_list = config.get_content_scan_list()
                scan.add_log("Retrieving number of pages")
                pages = _get_num_pages(base_url, config, auth_session)
                scan.add_log("There are %s pages of posts" % pages)
                for page in range(1, pages+1):
                    # if "homebuild" in config.website and page < 57:
                    #     continue
                    if page > 20 and not config.is_full_scan_needed:
                        break
                    try:
                        scan.add_log("Scanning page %s" % page)
                        _scan_page(page, base_url, config, auth_session, title_scan_list, content_scan_list, scan)
                    except:
                        st = get_stack_trace()
                        scan.add_log(st)
        except:
            st = get_stack_trace()
            scan.add_log(st)

        scan.end()