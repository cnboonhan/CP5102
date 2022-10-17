from lib.extract import IACExtractor
from lib.sso_models import SSOModel
import os
import json
import logging

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=LOGLEVEL)


if __name__ == '__main__':
    iac_path = os.environ.get('INFRASTRUCTURE_IAC_PATH', '.iac/kube_infra')

    sso = SSOModel()

    x = IACExtractor(iac_path=iac_path)
    x.extract_idp_config(sso)
    x.extract_authenticator_config(sso)

    with open("sso.json", "w") as outfile:
        json.dump(sso.describe(), outfile, indent=4)
