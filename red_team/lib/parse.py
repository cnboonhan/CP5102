import yaml


class IACParserOpenIDConnect():
  # Given files, identify and parse them to extract information useful for SSO
  # TODO: Assuming only one IDP for the moment
  def _load_idp_config(self, path: str):
    with open(path) as f:
      data = yaml.load(f, Loader=yaml.FullLoader)
      idp_config = data['identityProviders'][0]['config']
      return idp_config

  def get_idp_userinfo_endpoint(self, path: str):
    return self._load_idp_config(path)['userInfoUrl']

  def get_idp_token_endpoint(self, path: str):
    return self._load_idp_config(path)['tokenUrl']

  def get_idp_jwks_endpoint(self, path: str):
    return self._load_idp_config(path)['jwksUrl']

  def get_idp_auth_endpoint(self, path: str):
    return self._load_idp_config(path)['authorizationUrl']


class IACParserKubeNginx():
  def _load_kube_config(self, path: str):
    with open(path) as f:
      data = yaml.load_all(f, Loader=yaml.FullLoader)
      return list(data)

  # TODO: Implement rudimentary version of filtering to deduce path to keycloak service
  def get_login_page_path(self, path: str):
    return "https://cluster.cp5102.edu/auth"


class IACParserKubeCoreDNS():
  def _load_kube_config(self, path: str):
    with open(path) as f:
      data = yaml.load_all(f, Loader=yaml.FullLoader)
      return list(data)

  # TODO: Implement rudimentary version of extracting DNS resolution
  def get_idp_ip(self, path: str):
    return "172.28.0.1"

  # TODO: Implement rudimentary version of extracting DNS resolution
  def get_authenticator_ip(self, path: str):
    return "192.168.49.2"
