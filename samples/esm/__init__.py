import logging
import json
import requests

class EsmEvents(object):

    def __init__(self, url):
        self.url = url
        self.user = None
        self.password = None

    def case_created(self, event):
        logging.info("Sending case...")
        body = json.dumps(event)
        logging.info(json.dumps(event))
        #sys-log integration only
        #requests.post(self.url, data=body)

    def threat_created(self, event):
        logging.info("Sending threat...")
        logging.info(json.dumps(event))
        #requests.post(self.url, data=body)
