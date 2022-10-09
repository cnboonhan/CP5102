import graphviz


class IdentityProvider:
  def __init__(self):
    self.idp_userinfo_endpoint = None
    self.idp_auth_endpoint = None
    self.idp_jwks_endpoint = None
    self.idp_token_endpoint = None
    self.ip_address = None


class ServiceProvider:
  def __init__(self):
    self.jwks_endpoint = None
    self.idp_dns_name = None
    self.ip_address = None


class SSOModel:
  def __init__(self):
    self.idp = IdentityProvider()
    self.sp = ServiceProvider()

  def render(self):
    print("Rendering SSO Model")

    g = graphviz.Digraph('sso')
    g.node('IDP', 'IDP')  
    g.node('SP', 'SP')
    g.graph_attr['splines'] = 'false'

    g.edge('SP', 'IDP', label=f"token: {self.idp.idp_token_endpoint}")
    g.edge('SP', 'IDP', label=f"jwks: {self.idp.idp_jwks_endpoint}")
    g.edge('SP', 'IDP', label=f"userinfo: {self.idp.idp_userinfo_endpoint}")
    g.edge('SP', 'IDP', label=f"auth: {self.idp.idp_auth_endpoint}")
    g.render(directory='.').replace('\\', '/')
