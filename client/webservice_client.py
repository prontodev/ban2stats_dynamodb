from httplib2 import Http
from urllib import urlencode
from urlparse import urljoin


class BAN2STATSHandler(object):

    WEBSERVICE_HOST = 'http://localhost:8000'
    WEBSERVICE_HANDLER_URL = '/'

    def call_webservice_api(self):
        target_url = urljoin(self.WEBSERVICE_HOST, self.WEBSERVICE_HANDLER_URL)

        http = Http()
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {}
        body = urlencode(data)
        response, content = http.request(target_url, "POST", headers=headers, body=body)