#!/usr/bin/env python3

import urllib.request
import xml.etree.ElementTree as ET
import os

class NamesiloDNSRecord:
    version = 1
    query_type = "xml"
    api_root = "https://www.namesilo.com/api/"
    key = None
    host = None
    domain = None
    request_ip = None
    a_record = None
    rrid = None

    def __init__(self, key, host, domain):
        self.key = key
        self.host = host
        self.domain = domain
        self.setup()

    def setup(self):
        params = urllib.parse.urlencode({
            "version": self.version,
            "type": self.query_type,
            "key": self.key,
            "domain": self.domain
        })
        req = urllib.request.Request(self.api_root + "dnsListRecords?{}".format(params))
        # Namesilo does not like the default user agent and responds with 403 Forbidden
        req.add_header('User-Agent', '')
        with urllib.request.urlopen(req) as response:
            xml = response.read()
        tree = ET.fromstring(xml)
        self.request_ip = tree.find('./request/ip').text
        record = tree.find(".//resource_record[type='A'][host='{}.{}']".format(self.host, self.domain))
        self.a_record = record.find("./value").text
        self.rrid = record.find("./record_id").text

    def update(self, newip):
        params = urllib.parse.urlencode({
            "version": self.version,
            "type": self.query_type,
            "key": self.key,
            "domain": self.domain,
            "rrid": self.rrid,
            "rrhost": self.host,
            "rrvalue": newip,
            "rrttl": 3600
        })
        req = urllib.request.Request(self.api_root + "dnsUpdateRecord?{}".format(params))
        req.add_header('User-Agent', '')
        urllib.request.urlopen(req)


if __name__ == "__main__":
    print("Checking domain status")

    KEY = os.environ.get("NAMESILO_KEY")
    HOST = os.environ.get("NAMESILO_HOST")
    DOMAIN = os.environ.get("NAMESILO_DOMAIN")

    if None in [KEY, HOST, DOMAIN]:
        print("Please set the environemnt variables")
        exit(1)

    ns = NamesiloDNSRecord(KEY, HOST, DOMAIN)

    if ns.a_record != ns.request_ip:
        print("Updating A record")
        ns.update(ns.request_ip)
    else:
        print("Nothing to do")
