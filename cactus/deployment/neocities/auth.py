#coding:utf-8
from cactus.deployment.auth import BaseKeyringCredentialsManager

class NeocitiesCredentialsManager(BaseKeyringCredentialsManager):
    _username_config_entry = "neocities-credentials"
    _username_display_name = "Neocities Site Name"
    _password_display_name = "Neocities Account Password"
    _keyring_service = "cactus/neocities"
