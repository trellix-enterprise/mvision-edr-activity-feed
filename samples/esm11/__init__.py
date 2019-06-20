"""
MCAFEE CONFIDENTIAL
Copyright (c) 2019 McAfee, LLC
The source code contained or described herein and all documents related
to the source code ("Material") are owned by McAfee or its
suppliers or licensors. Title to the Material remains with McAfee
or its suppliers and licensors. The Material contains trade
secrets and proprietary and confidential information of McAfee or its
suppliers and licensors. The Material is protected by worldwide copyright
and trade secret laws and treaty provisions. No part of the Material may
be used, copied, reproduced, modified, published, uploaded, posted,
transmitted, distributed, or disclosed in any way without McAfee's prior
express written permission.
No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or
delivery of the Materials, either expressly, by implication, inducement,
estoppel or otherwise. Any license under such intellectual property rights
must be express and approved by McAfee in writing.
"""

from mvision_edr_activity_feed import subscribe
from samples.esm import EsmEvents
from logging.handlers import SysLogHandler
import logging

"""
ESM11 subscription to Threat and Case entities:
Please notice that SysLogHandler is set locally and then its recommended to:
1.Point rsyslog.conf to REMOTE ESM
2.Enable TLS for secured communication instead of UDP
(ASP Passive DS must be enabled for TLS too so Threat evidence packets can't
be expossed to Man In de Middle attacks)
"""
esm_events = None

def setup():
    global esm_events
    if not esm_events:
        esm_events = EsmEvents()
        try:
            logging.info("***About to setup SysLogHandler for ESM...")
            # SysLog support at Sample level -Perhaps is better at global level.
            # SysLogHandler configured to local syslog and it requires that the
            # user configures rsyslog.conf to point to remote ESM because:
            # 1. TLS can be configured from local sys log to remote ESM (In order to avoid Man in the Middle Attack)
            # 2. More performant as rsyslog can be configured to send batches
            # Anyways, if the SDK client developer decides to not point lolcally simply pass url to SysLogHandler: 
            # handler = SysLogHandler(address=('ESM_REMOTE_SERVER_IP', UDP_OR_TLS_PORT))
            logger = logging.getLogger()
            handler = SysLogHandler(address='/dev/log')
            # Logging level must be info for SysLogHandler in order to send proper information:
            handler.setLevel(logging.INFO)
            logger.addHandler(handler)
            logging.info("***SysLogHandler setup successfull!")
            # Default log location in case needed at sudo level for investigating payloads.
            # Normally commented as it needs to be run as sudo but it can be used for troubleshoot purposes:
            #logger.addHandler(logging.FileHandler("/var/log/mvedr_activity_feed_esm.log"))
        except Exception as e:
            logging.error("***Error while setting up SysLogHandler or FileHandler for ESM")

# @subscribe(entity='case')
# def any_case_event(event):
#     logging.info("ESM CASE EVENT: %s", event)
#     setup()
#     esm_events.send_case(event)

@subscribe(entity='threat')
def any_threat_event(event):
    logging.info("ESM THREAT EVENT: %s", event)
    setup()
    esm_events.send_threat(event)
    
