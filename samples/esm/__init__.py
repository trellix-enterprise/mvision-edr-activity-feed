import logging
import json

class EsmEvents(object):
        
    def send_case(self, event):
        logging.debug(">>>Sending ESM case...")
        # It uses SysLogHandler configured in esm main module so we only need to dump the Case event:
        logging.info(json.dumps(event))
        
    def send_threat(self, event):
        # It uses SysLogHandler configured in esm main module so we only need to dump the Threat event:
        logging.debug(">>>Sending ESM threat...")
        logging.info(json.dumps(event))
