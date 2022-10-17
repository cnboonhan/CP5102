# -*- coding: utf-8 -*-
import socket
from typing import Tuple, Optional

from proxy.http.proxy import HttpProxyBasePlugin
from proxy.common.types import HostPort


class CP5102DnsResolverPlugin(HttpProxyBasePlugin):

    def resolve_dns(self, host: str, port: int) -> Tuple[Optional[str], Optional[HostPort]]:
        print("I'm IN")
        try:
            return socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)[0][4][0], None
        except socket.gaierror:
            # Ideally we can also thrown HttpRequestRejected or HttpProtocolException here
            # Returning None simply fallback to core generated exceptions.
            return None, None
