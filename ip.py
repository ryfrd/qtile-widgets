from libqtile.widget import base

import requests

class IP(base.ThreadPoolText):

    defaults = [
        ("update_interval", 60, "Update interval for the IP widget"),
        ("format","{country}: {ip}","IP display format",),
    ]

    def __init__(self, **config):
        super().__init__("", **config)
        self.add_defaults(IP.defaults)

    def poll(self):
        ip_info = requests.get("https://ipinfo.io").json()
        variables = {
            "ip": ip_info["ip"],
            "country": ip_info["country"],
            "region": ip_info["region"],
            "city": ip_info["city"],
        }
        return self.format.format(**variables)
