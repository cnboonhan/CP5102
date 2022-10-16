from lib.extract import IACExtractor
from lib.sso_models import SSOModel
import os
import logging
from mitmproxy import http
from mitmproxy import ctx
import asyncio
import sys
from mitmproxy import options
from mitmproxy.tools import dump

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=LOGLEVEL)


class RequestLogger:
    def __init__(self, sso):
        self.sso = sso

    def request(self, flow: http.HTTPFlow) -> None:
        logging.debug(flow)
        if flow.request and flow.request.method == 'POST':
            if self.sso.idp.domain:
                logging.info(flow.request.pretty_url)
                if (self.sso.idp.domain in flow.request.pretty_url):
                    logging.info(
                        f"Intercepted Request: {flow.request.urlencoded_form}")


async def start_proxy(host, port, sso: SSOModel):
    opts = options.Options(
        listen_host=host, listen_port=port, ssl_insecure=True)

    master = dump.DumpMaster(
        opts,
        with_termlog=False,
        with_dumper=False,
    )

    master.addons.add(RequestLogger(sso))

    await master.run()
    return master


if __name__ == '__main__':
    iac_path = os.environ.get('INFRASTRUCTURE_IAC_PATH', 'kube-infra')

    sso = SSOModel()

    x = IACExtractor(iac_path=iac_path)
    x.extract_idp_config(sso)
    x.extract_authenticator_config(sso)

    logging.info("Starting Request Logger.")
    asyncio.run(start_proxy("0.0.0.0", 5000, sso))
    logging.info("Terminated Request Logger.")
