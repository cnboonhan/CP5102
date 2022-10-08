from abc import ABC, abstractmethod


# Given a set of IAC files, extract the paths of files relevant for SSO
class IACExtractor(ABC):
  @abstractmethod
  def extract_authenticator_config(self):
    pass

  @abstractmethod
  def extract_ingress_config(self):
    pass

  @abstractmethod
  def extract_dns_config(self):
    pass

  @abstractmethod
  def extract_domain_name(self):
    pass


class DemoIACExtractor(IACExtractor):
  # TODO: Hardcoded return for PoC, full implementation is to use pattern matching logic to identify the most likely file to fall under these SSO component categories
  def extract_domain_name(self):
    return "cluster.cp5102.edu"

  def extract_authenticator_config(self):
    return "iac/docker/keycloak/realms.json"

  def extract_ingress_config(self):
    return "iac/k8s/ingress.yaml"

  def extract_dns_config(self):
    return "iac/k8s/coredns.yaml"
