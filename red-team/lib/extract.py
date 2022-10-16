from lib.sso_models import SSOModel
from lib.extract_helpers import extract_authenticator_keycloak_realms_config, extract_authenticator_keycloak_ingress_config, extract_kubernetes_dns_coredns_configs
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

        # TODO: Implement more Info objects for different Authenticators
        realms_config = extract_authenticator_keycloak_realms_config(
            self.all_non_hidden_files_in_iac_path)
        if realms_config:
            # TODO: For now, just select the IDP with hardcoded 'oidc' for demo purposes
            c = realms_config.idp_configs['oidc']
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

    def extract_authenticator_config(self, sso: SSOModel):
        logging.info(f"Extracting Authenticator configurations..")

        realms_config = extract_authenticator_keycloak_realms_config(
            self.all_non_hidden_files_in_iac_path)
        ingress_config = extract_authenticator_keycloak_ingress_config(
            self.all_non_hidden_files_in_iac_path)
        dns_configs = extract_kubernetes_dns_coredns_configs(self.all_non_hidden_files_in_iac_path)

        if realms_config and ingress_config and dns_configs:
            # TODO: For now, just select the IDP with hardcoded 'oidc' for demo purposes
            c = realms_config.idp_configs['oidc']
            sso.authenticator.realm = realms_config.realm

            for dns_config in dns_configs:
                hosts_re = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}'
                all_hosts = re.findall(hosts_re, dns_config.config)
            # TODO: Currently manual selection from all_hosts from dns config
            sso.authenticator.domain = "cluster.cp5102.edu"
            sso.authenticator.authorizationUrl = f"{sso.authenticator.domain}{ingress_config.ingress_path}/realms/{realms_config.realm}/protocol/openid-connect/auth"

            logging.info(
                f"SSO Model after authenticator config extraction: {sso.describe()}")
            return


