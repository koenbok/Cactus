#coding:utf-8
import logging
import requests
from pprint import pprint

from cactus.deployment.engine import BaseDeploymentEngine
from cactus.deployment.neocities.auth import NeocitiesCredentialsManager
from cactus.deployment.neocities.rest.list import NeocitiesList
from cactus.deployment.neocities.rest.upload import NeocitiesUpload
from cactus.deployment.neocities.rest.delete import NeocitiesDelete

logger = logging.getLogger(__name__)

class NeocitiesDeploymentEngine(BaseDeploymentEngine):
    CredentialsManagerClass = NeocitiesCredentialsManager

    def __init__(self, *args, **kwargs):
        super(NeocitiesDeploymentEngine, self).__init__(*args, **kwargs)
        self.site.compress_extensions = [] # No compression

    def deploy(self):
        self.configure()
        result = self.upload()
        if result:
            self.credentials_manager.save_credentials()
            return map(lambda file: {'changed': True, 'size': len(file.payload())}, self.files())
        else:
            return []

    """
    NeocitiesDeploymentEngine.configure()
    Overloaded from base class in order to simplify, we only need to get the user's credentials and load our API classes
    """
    def configure(self):
        user, password = self.credentials_manager.get_credentials()

        self.list_api = NeocitiesList(user,password)
        self.upload_api = NeocitiesUpload(user,password)
        self.delete_api = NeocitiesDelete(user,password)

        logger.info("Set upload path to site: " + user)


    """
    NeocitiesDeploymentEngine.upload()
    Overloaded from base class 

    This uses the Neocities List API to get the files currently on the server.
    Based on those files, it will upload any files that have since been updated locally (based on updated_at dates)
    and delete any files that are no longer exist locally

    This COULD be smarter; to update only files that need changing, but in theory a full blow-away and reload is
    better from a deployment perspective.  This becomes a philosophical issue rather than a technical one.

    @return bool
    """
    def upload(self):
        try:
            logger.info("Recieving information from " + self.list_api.sitename + "...")
            apifiles = self.list_api.call()

            logger.info("Cleaning server for fresh deploy...")
            for f in apifiles['files']:
                if(self.is_root(f) and f['path'] != "index.html"):
                    self.delete_api.add_file(f['path'])
            self.delete_api.call()

            logger.info("Uploading files to server...")
            for f in self.files():
                self.upload_api.add_file(f)
            self.upload_api.call()

        except Exception as e:
            logger.error(e)
            return False
        else:
            return True

    def is_root(self, file):
        return file["path"].find("/") == -1
