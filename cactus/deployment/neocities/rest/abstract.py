#coding:utf-8
import requests
import logging
import json
from pprint import pprint

from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

class NeocitiesRestAbstract(object):
    ApiEndpoint = "https://neocities.org/api/"
    DataFilter = False # If the endpoint needs data, set this to true in child class

    def __init__(self, sitename, password):
        self.sitename = sitename
        self.password = password

        self.data = []

        if not self.sitename:
            raise "Invalid sitename error"

        self.request = requests.Request(self.get_method(), self.get_endpoint(), auth=self.get_auth())

    def call(self):
        if self.validate_data() == False:
            return False

        if(self._before_call() != False):
            prepared_req = self.request.prepare()
            session = requests.Session()

            response = self.handleResponse(session.send(prepared_req))

            session.close()

            return response

    def _before_call(self):
        pass

    def validate_data(self):
        if self.DataFilter == False:
            return True
        else:
            return len(self.data) > 0

    """
    NeocitiesRestAbstract.handleResponse()
    @return string message body
    @raise Exception
    """
    def handleResponse(self, response):
        try:
            body = json.loads(response.content)
            response.raise_for_status()
        except requests.HTTPError:
            raise Exception("Request returned " + str(response.status_code) + ": " + body['message'])
        except Exception:
            raise Exception("API call to " + self.get_endpoint() + " failed")
        else:
            if body["result"] != "success": raise Exception("Neocities returned an unsuccessful status: " + body['message'])
            return body

    def get_auth(self):
        return HTTPBasicAuth(self.sitename, self.password)

    def get_endpoint(self):
        return self.ApiEndpoint + self.Action

    def get_action(self):
        return self.Action

    def get_method(self):
        return self.Method

