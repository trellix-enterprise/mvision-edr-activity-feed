import logging
import json

class EsmEvents(object):
        
    def send_case(self, event):
        logging.debug(">>>Sending ESM case...")
        logging.info(json.dumps(event))
        
    def send_threat(self, event):
        logging.debug(">>>Sending ESM threat...")
        logging.info(json.dumps(event))
