from lib.sso_models import SSOModel
from lib.extract_helpers import extract_authenticator_keycloak_realms_config, extract_authenticator_keycloak_ingress_config
import glob
import re
import os
import logging


class IACExtractor:
    def __init__(self, iac_path: str):
        all_glob_files = glob.glob(iac_path + '/**', recursive=True)
        self.all_non_hidden_files_in_iac_path = [
            os.path.abspath(f) for f in all_glob_files if not f.startswith('.')]
        logging.info("Initializing IAC Extractor")
        logging.debug(f"All Files: {all_glob_files}")
        logging.debug(
            f"All Possible IAC Paths: {self.all_non_hidden_files_in_iac_path}")

    def extract_idp_config(self, sso: SSOModel):
        logging.info(f"Extracting IDP configurations..")
        config = extract_authenticator_keycloak_realms_config(
            self.all_non_hidden_files_in_iac_path)
        if config:
            # TODO: For now, just select the IDP with hardcoded 'oidc' for demo purposes
            c = config.idp_configs['oidc']
            sso.idp.userInfoUrl = c.userInfoUrl
            sso.idp.tokenUrl = c.tokenUrl
            sso.idp.jwksUrl = c.jwksUrl
            sso.idp.authorizationUrl = c.authorizationUrl
            sso.idp.domain = None
            m = re.search('https?://([A-Za-z_0-9.-]+).*',
                          sso.idp.authorizationUrl)
            if m:
                sso.idp.domain = m.group(1)

            logging.info(
                f"SSO Model after idp info extraction: {sso.describe()}")
            return
        # TODO: Implement more Info objects for different Authenticators

    def extract_serviceprovider_config(self, sso: SSOModel):
        logging.info(f"Extracting ServiceProvider configurations..")
        config = extract_authenticator_keycloak_ingress_config(
            self.all_non_hidden_files_in_iac_path)
