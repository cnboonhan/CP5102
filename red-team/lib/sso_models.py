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


class SSOModel:
    def __init__(self):
        self.idp = IDP()  # type: IDP

    def describe(self):
        return {'idp': self.idp.__dict__}
