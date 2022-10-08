from lib.extract import DemoIACExtractor
from lib.identify import DemoIACIdentifier
from lib.parse import IACParserOpenIDConnect, IACParserKubeNginx, IACParserKubeCoreDNS
from lib.sso_model import SSOModel

if __name__ == '__main__':
  print("\n-------------------EXTRACTING SSO COMPONENT IAC--------------------------")
  x = DemoIACExtractor()
  dns_config = x.extract_dns_config()
  ingress_config = x.extract_ingress_config()
  authenticator_config = x.extract_authenticator_config()
  domain_name = x.extract_domain_name()

  print(f"DNS Config Path: {dns_config}")
  print(f"Ingress Config Path: {ingress_config}")
  print(f"Authenticator Config Path: {authenticator_config}")
  print(f"Domain Name: {domain_name}")
  
  print("\n-------------------EXTRACTING AUTHENTICATOR CONFIG-----------------------00")
  authenticator_config_type = DemoIACIdentifier().identify_authenticator_config(authenticator_config)
  print(f"Authenticator Config type identified as {authenticator_config_type}")

  openid_parser = IACParserOpenIDConnect() 
  idp_userinfo_endpoint = openid_parser.get_idp_userinfo_endpoint(authenticator_config)
  idp_auth_endpoint = openid_parser.get_idp_auth_endpoint(authenticator_config)
  idp_jwks_endpoint = openid_parser.get_idp_jwks_endpoint(authenticator_config)
  idp_token_endpoint = openid_parser.get_idp_token_endpoint(authenticator_config)
  print(f"Authentication Userinfo Endpoint: {idp_userinfo_endpoint}")
  print(f"Authentication Auth Endpoint: {idp_auth_endpoint}")
  print(f"Authentication JWKS Endpoint: {idp_jwks_endpoint}")
  print(f"Authentication Token Endpoint: {idp_token_endpoint}")

  print("\n-------------------EXTRACTING INGRESS CONFIG-------------------------------")
  ingress_config_type = DemoIACIdentifier().identify_ingress_config(ingress_config)
  print(f"Ingress Config type identified as {ingress_config_type}")

  kube_nginx_parser = IACParserKubeNginx()
  ingress_login_path = kube_nginx_parser.get_login_page_path(ingress_config)
  print(f"Ingress Login Page: {ingress_login_path}")

  print("\n-------------------EXTRACTING DNS CONFIG-----------------------------------")
  dns_config_type = DemoIACIdentifier().identify_dns_config(dns_config)
  print(f"DNS Config type identified as {dns_config_type}")

  kube_coredns_parser = IACParserKubeCoreDNS()
  idp_ip = kube_coredns_parser.get_idp_ip(dns_config)
  authenticator_ip = kube_coredns_parser.get_authenticator_ip(dns_config)
  print(f"IDP IP Address: {idp_ip}")
  print(f"Authenticator IP Address: {authenticator_ip}")


  print("\n-------------------Generating SSO Model-----------------------------------")
  sso = SSOModel()
