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

"""Example of subscription to case-related events, and
integration with The Hive
"""
from mvision_edr_activity_feed import subscribe

from samples.thehive.api import TheHiveApiClient
from samples.thehive.tenant import Tenant

tenant = None
hive_api_client = None


def setup(config):
    """Setup global connection to The hive using callback configuration
    parameters:
    * hive_user: The user to assign the cases in The Hive
    * hive_url: The URL for The Hive server
    * hive_key: The API key for The Hive server
    """
    global tenant, hive_api_client
    if not tenant and not hive_api_client:
        tenant = Tenant(config.hive_user, config.hive_url, config.hive_key)
        hive_api_client = TheHiveApiClient(tenant)


@subscribe(entity='case', subtype='creation')
def case_created(event, config):
    setup(config)
    hive_api_client.create_case(event)


@subscribe(entity='case', subtype='priority-update')
def case_priority_updated(event, config):
    setup(config)
    hive_api_client.update_case_priority(event)


@subscribe(entity='case', subtype='status-update')
def case_status_updated(event, config):
    setup(config)
    hive_api_client.update_case_status(event)
