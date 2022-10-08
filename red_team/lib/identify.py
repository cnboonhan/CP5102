from abc import ABC, abstractmethod


# Given IAC file of each SSO component, identify the implementation of each component to inform how to parse the file contents
class IACIdentifier(ABC):
  @abstractmethod
  def identify_authenticator_config(self, config):
    pass

  @abstractmethod
  def identify_ingress_config(self, config):
    pass

  @abstractmethod
  def identify_dns_config(self, config):
    pass


class DemoIACIdentifier(IACIdentifier):
  # TODO: Hardcoded Type for PoC: Further refinement is to pick out implementation specific details
  def identify_authenticator_config(self, config):
    return "openid/keycloak"

  def identify_ingress_config(self, config):
    return "k8s/nginx"

  def identify_dns_config(self, config):
    return "coredns"
