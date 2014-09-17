from httplib2 import Http
from urllib import urlencode
from urlparse import urljoin


class BAN2STATSHandler(object):

    WEBSERVICE_HOST = 'http://localhost:8000'
    BAN2STATS_HANDLER_URL = '/'

    def api_url(self):
        return urljoin(self.WEBSERVICE_HOST, self.BAN2STATS_HANDLER_URL)

    def call_webservice_api(self):
        http = Http()
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {}
        body = urlencode(data)
        response, content = http.request(self.api_url(), "POST", headers=headers, body=body)
        return response, content