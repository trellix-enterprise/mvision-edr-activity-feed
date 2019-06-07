import requests
from logging.handlers import SysLogHandler
import logging
import json

class EsmEvents(object):

    def __init__(self, url):
        self.url = url
        # SysLog support at Sample level -Perhaps is better at global level.
        # SysLogHandler configured to local syslog and it requires that the
        # user configures rsyslog.conf to point to remote ESM because:
        # 1. TLS can be configured from local sys log to remote ESM (In order to avoid Man in the Middle Attack)
        # 2. More performant as rsyslog can be configured to send batches
        # Anyways, ut the SDK client developer decides to not poin tolcally simply pass url to SysLogHandler: 
        # handler = SysLogHandler(address=('ESM_REMOTE_SERVER_IP', UDP_OR_TLS_PORT))
        logger = logging.getLogger()
        handler = SysLogHandler(address='/dev/log')
        # Logging level must be info for SysLogHandler in order to send proper information:
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        # Default log location in case needed at sudo level for investigating payloads.
        # Normally commented as it needs to be run as sudo:
        logger.addHandler(logging.FileHandler("/var/log/mvedr_activity_feed.log"))
        
    def send_case(self, event):
        logging.debug(">>>Sending ESM case...")
        logging.info(json.dumps(event))
        
    def send_threat(self, event):
        logging.debug(">>>Sending ESM threat...")
        logging.info(json.dumps(event))
