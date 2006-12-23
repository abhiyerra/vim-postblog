# Post to Blogger API
# Copyright (c) 2006 Kesava Yerra. Licensed under BSD.

import httplib
import urllib
import urllib2
from xml.dom.minidom import Document

class GoogleLogin:
    def __init__(self, email, passwd, service):
        params = urllib.urlencode({'Email': email, 
                                   'Passwd': passwd,
                                   'service': service,
                                   'source': 'upbylunch-1'})
        headers = {"Content-type": "application/x-www-form-urlencoded"}

        conn = httplib.HTTPSConnection("www.google.com")
        conn.request("POST", "/accounts/ClientLogin", params, headers)

        response = conn.getresponse()
        data = response.read()

        # If the login fails Google returns 403
        if response.status == 403:
            self.auth = None
        else:
            self.auth = data.splitlines()[2].split('=')[1]

        conn.close()

    def get_auth(self):
        return self.auth

class BloggerGDataService:
    def __init__(self, auth, blogid):
        self.auth = auth
        self.blogid = blogid

    def insert_entry(self, entry, host='', path=''):
        if host == '':
            host = 'www.blogger.com'

        if path == '':
            path = '/feeds/%s/posts/default' % (self.blogid)

        headers = {"Authorization": "GoogleLogin auth=%s" % self.auth,
                   "Content-type": "application/atom+xml"}

        conn = httplib.HTTPConnection(host)
        conn.request("POST", path, entry, headers)

        res = conn.getresponse()

        if res.status == 302:
            location = res.getheader('location')[7:].split('/', 1)
            host = location[0]
            path = '/' + location[1]
            
            self.insert_entry(entry, host, path)
        else:
            print res.reason


class Entry:
    def __init__(self, title, content, labels):
        self.title = title
        self.content = content
        self.labels = labels

    def _get_label_element(self, label):
        return '<category term="%s"/>\n' % label.replace(' ', '+')

    def __str__(self):
        xml_entry = \
            """
            <entry xmlns='http://www.w3.org/2005/Atom'>
              <title type='text'>%s</title>
              %s
              <content type="xhtml">%s</content>
            </entry>
            """ % (self.title, 
                   ''.join([self._get_label_element(label) for label in self.labels.split(', ')]),
                   self.content)

        return xml_entry

def post_entry(email, passwd, blogid, title, content, labels):
    entry = Entry(title, content, labels)

    gl = GoogleLogin(email, passwd, 'blogger')

    blogger = BloggerGDataService(gl.get_auth(), blogid)
    blogger.insert_entry(str(entry))

post_entry('email', 'password', 'postid', 'Test', '<p>Test</p><p>Test2</p>', 'test1, test2, test3')
