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

sudo mvision-edr-activity-feed --url https://api.soc.mcafee.com/ --username {USER} --password {PASS} --module samples.splunk --loglevel=debug
"""

from mvision_edr_activity_feed import subscribe
from logging.handlers import SysLogHandler
import logging
import json

logging.debug("Imported: %s", __name__)

def setup():
    try:
        logging.info("***About to setup SysLogHandler ...")
        logger = logging.getLogger()
        handler = SysLogHandler(address='/dev/log')
        # Logging level must be info for SysLogHandler in order to send proper information:
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        logging.info("***SysLogHandler setup successfull!")
    except Exception as e:
        logging.error("***Error while setting up SysLogHandler or FileHandler for Splunk")


# uncomment as needed:            
# @subscribe(entity='threat')
def send_threat(event):
    # uncomment as needed:
    """
    setup()
    logging.info(json.dumps(event))
    """
    
# uncomment as needed:    
# @subscribe(entity='case')
def any_case_event(event):
    # uncomment as needed:
    """
    setup()
    logging.info(json.dumps(event))
    """
