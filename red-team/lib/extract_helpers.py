from lib.config import GlobalConfigurations
from typing import List
import jsonschema
import yamale
import logging
import json
import yaml


class AuthenticatorKeycloakRealmsInfo:
    class IDPConfigInfo:
        def __init__(self, userInfoUrl: str, tokenUrl: str, jwksUrl: str, authorizationUrl: str):
            self.userInfoUrl = userInfoUrl
            self.tokenUrl = tokenUrl
            self.jwksUrl = jwksUrl
            self.authorizationUrl = authorizationUrl

    def __init__(self, iac_filepath: str):
        self.id = None
        self.idp_configs = {}
        logging.info(
            f"Parsing {iac_filepath} as an {self.__class__.__name__} object")

        with open(iac_filepath) as iac:
            iac_json = json.load(iac)
            self.id = iac_json['id']
            for idp in iac_json['identityProviders']:
                alias = idp['alias']
                config = idp['config']
                self._add_idp_config(
                    alias, config['userInfoUrl'], config['tokenUrl'], config['jwksUrl'], config['authorizationUrl'])

    def _add_idp_config(self, alias: str, userInfoUrl: str, tokenUrl: str, jwksUrl: str, authorizationUrl: str):
        self.idp_configs[alias] = (self.IDPConfigInfo(
            userInfoUrl, tokenUrl, jwksUrl, authorizationUrl))


class AuthenticatorKeycloakIngressInfo:
    def __init__(self, ingress_path: str):
        self.ingress_path = ingress_path


def extract_authenticator_keycloak_realms_config(files: List[str]):
    with open(GlobalConfigurations.AUTHENTICATOR_KEYCLOAK_REALMS_SCHEMA) as schema_filepath:
        schema = json.load(schema_filepath)
        logging.debug(
            f"Scanning for Keycloak Realms file using {GlobalConfigurations.AUTHENTICATOR_KEYCLOAK_REALMS_SCHEMA} with schema {schema}")

        for iac_filepath in files:
            try:
                with open(iac_filepath) as iac:
                    logging.debug(f"Opening {iac_filepath}")
                    jsonschema.validate(
                        instance=json.load(iac), schema=schema)
                    logging.info(
                        f"{iac_filepath} is valid Keycloak Realms file with IDP configuration.")
                return AuthenticatorKeycloakRealmsInfo(iac_filepath)
            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                logging.debug(f"{iac_filepath} is not a json file")
            except jsonschema.ValidationError as e:
                logging.debug(e)
                logging.debug(f"{iac_filepath} failed validation.")
            except IsADirectoryError:
                continue

    logging.warning(f"No valid Authenticator IAC was found")
    return None


def extract_authenticator_keycloak_ingress_config(files: List[str]):
    def _get_keycloak_selector(files) -> str | None:
        schema = yamale.make_schema(
            GlobalConfigurations.AUTHENTICATOR_KEYCLOAK_KUBERNETES_DEPLOYMENT_SCHEMA)
        logging.info(
            f"Scanning for Keycloak Kubernetes Deployment using {GlobalConfigurations.AUTHENTICATOR_KEYCLOAK_KUBERNETES_DEPLOYMENT_SCHEMA} with schema {schema.dict}")

        for iac_filepath in files:
            try:
                with open(iac_filepath) as iac:
                    datas = yaml.load_all(iac, Loader=yaml.SafeLoader)
                    logging.debug(schema.dict)
                    for data in datas:
                        try:
                            is_valid = yamale.validate(schema, yamale.make_data(
                                content=yaml.dump(data)), strict=False)
                            if is_valid:
                                logging.info(f"Found deployment for a keycloak image in file {iac_filepath}")
                                return data['spec']['selector']['matchLabels']['app']  

                        except yamale.yamale_error.YamaleError as e:
                            # logging.debug(e)
                            continue

                    logging.debug(f"{iac_filepath} failed validation.")

            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                logging.debug(f"{iac_filepath} is not a yaml file")
            except IsADirectoryError:
                continue
        logging.warning(f"No valid Deployment IAC was found")

    def _get_keycloak_service(files, selector_id: str):
        schema = yamale.make_schema(
            GlobalConfigurations.AUTHENTICATOR_KEYCLOAK_KUBERNETES_SERVICE_SCHEMA)
        logging.info(
            f"Scanning for Keycloak Kubernetes Service using {GlobalConfigurations.AUTHENTICATOR_KEYCLOAK_KUBERNETES_SERVICE_SCHEMA} with schema {schema.dict}")

        for iac_filepath in files:
            try:
                with open(iac_filepath) as iac:
                    datas = yaml.load_all(iac, Loader=yaml.SafeLoader)
                    for data in datas:
                        try:
                            is_valid = yamale.validate(schema, yamale.make_data(
                                content=yaml.dump(data)), strict=False)
                            if is_valid and data['spec']['selector']['app'] == selector_id:
                                logging.info(f"Found Service for a keycloak Deployment in file {iac_filepath} and selector {selector_id}")
                                return data['metadata']['name']

                        except yamale.yamale_error.YamaleError as e:
                            # logging.debug(e)
                            continue

                    logging.debug(f"{iac_filepath} failed validation.")

            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                logging.debug(f"{iac_filepath} is not a yaml file")
            except IsADirectoryError:
                continue
        logging.warning(f"No valid Service IAC was found")

    def _get_keycloak_ingress(files, service_name: str):
        schema = yamale.make_schema(
            GlobalConfigurations.AUTHENTICATOR_KEYCLOAK_KUBERNETES_INGRESS_SCHEMA)
        logging.info(
            f"Scanning for Keycloak Kubernetes Ingress using {GlobalConfigurations.AUTHENTICATOR_KEYCLOAK_KUBERNETES_INGRESS_SCHEMA} with schema {schema.dict}")

        for iac_filepath in files:
            try:
                with open(iac_filepath) as iac:
                    datas = yaml.load_all(iac, Loader=yaml.SafeLoader)
                    for data in datas:
                        try:
                            is_valid = yamale.validate(schema, yamale.make_data(
                                content=yaml.dump(data)), strict=False)
                            if is_valid:
                                rules = data['spec']['rules']
                                for rule in rules:
                                    paths = rule['http']['paths']
                                    for path in paths:
                                        backend = path['backend']['service']['name']
                                        if backend == service_name:
                                            logging.info(f"Found Ingress for a keycloak Service in file {iac_filepath} and service name {service_name}")
                                            return path['path']

                        except yamale.yamale_error.YamaleError as e:
                            # logging.debug(e)
                            continue

                    logging.debug(f"{iac_filepath} failed validation.")

            except (json.decoder.JSONDecodeError, UnicodeDecodeError):
                logging.debug(f"{iac_filepath} is not a yaml file")
            except IsADirectoryError:
                continue
        logging.warning(f"No valid Service IAC was found")


    selector_id = _get_keycloak_selector(files)
    if not selector_id:
        return None
    logging.info(f"Identified keycloak selector ID: {selector_id}")

    service_name = _get_keycloak_service(files, selector_id)
    if not service_name:
        return None
    logging.info(f"Identified keycloak service name: {service_name}")

    ingress_path = _get_keycloak_ingress(files, service_name)
    if ingress_path:
        return AuthenticatorKeycloakIngressInfo(ingress_path)
