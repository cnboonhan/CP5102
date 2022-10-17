import logging
from typing import Dict
import json


class IDP:
    def __init__(self):
        self.userInfoUrl = None          # type: str | None
        self.tokenUrl = None             # type: str | None
        self.jwksUrl = None              # type: str | None
        self.authorizationUrl = None     # type: str | None
        self.domain = None               # type: str | None
        self.clientId = None              # type: str | None


class Authenticator:
    def __init__(self):
        self.realm = None                # type: str | None
        self.domain = None               # type: str | None
        self.authorizationUrl = None     # type: str | None


class SSOModel:
    def __init__(self):
        self.idp = IDP()
        self.authenticator = Authenticator()

    def describe(self):
        return {'idp': self.idp.__dict__, 'authenticator': self.authenticator.__dict__}

    def load_from_json(self, data):
        try:
            self.idp.userInfoUrl = data['idp']['userInfoUrl']
            self.idp.tokenUrl = data['idp']['tokenUrl']
            self.idp.jwksUrl = data['idp']['jwksUrl']
            self.idp.authorizationUrl = data['idp']['authorizationUrl']
            self.idp.domain = data['idp']['domain']
            self.idp.clientId = data['idp']['clientId']
            self.authenticator.realm = data['authenticator']['realm']
            self.authenticator.domain = data['authenticator']['domain']
            self.authenticator.authorizationUrl = data['authenticator']['authorizationUrl']
        except Exception as e:
            logging.critical(e)
