#coding:utf-8
import logging
from pprint import pprint

from cactus.deployment.neocities.rest.abstract import NeocitiesRestAbstract

logger = logging.getLogger(__name__)

class NeocitiesUpload(NeocitiesRestAbstract):
    Action = "upload"
    Method = "POST"
    DataFilter = True

    def add_file(self, file):
        self.data.append(file)
        
    def _before_call(self):
        self.request.files = map(lambda file: (file.url, file.payload()), self.data)