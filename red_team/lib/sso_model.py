class IdentityProvider:
  def __init__(self):
    self.dns_name = None
    self.client_id = None
    self.well_known_configuration_url = None


class ServiceProvider:
  def __init__(self):
    self.dns_name = None
    self.jwks_endpoint = None
    self.idp_dns_name = None


class SSOModel:
  def __init__(self):
    self.idp = IdentityProvider()
    self.sp = ServiceProvider()
