#coding:utf-8
import logging
from pprint import pprint

from cactus.deployment.neocities.rest.abstract import NeocitiesRestAbstract

logger = logging.getLogger(__name__)

class NeocitiesDelete(NeocitiesRestAbstract):
    Action = "delete"
    Method = "POST"
    DataFilter = True

    def add_file(self, file):
        self.data.append(file)

    def _before_call(self):
        self.request.data = {
            "filenames[]": self.data
        }