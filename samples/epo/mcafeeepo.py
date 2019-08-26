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
import json
import logging
import os

from mvision_edr_activity_feed import subscribe
from samples.epo import mcafee

"""Example of McAfee ePO threat event creation

Generate an ePO Threat Event with info provided by MVISION EDR activity feed 

Usage:
/python -m mvision_edr_activity_feed --consumer-group <test_consumer_group> 
                                     --url <mvision_edr_url> 
                                     --username <mvision_edr_username> 
                                     --password <mvision_edr_password> 
                                     --module samples.epo.mcafeeepo 
                                     --loglevel=debug 
                                     --config host=<epo_host> 
                                     --config port=<epo_port>
                                     --config username=<epo_username> 
                                     --config password=<epo_password>

"""

THRESHOLD_SCORE = 70
THREAT_EVENT_REMOTE_COMMAND = "DxlBrokerMgmt.createEpoThreatEvent"
epo_client = None


@subscribe(entity='threat')
def threat_event(event, config):
    try:

        if int(event["threat"]["score"]) >= THRESHOLD_SCORE:
            # connect to McAfee ePO
            global epo_client
            if epo_client is None:
                epo_client = connect(config)

            if epo_client is None:
                logging.error("McAfee ePO client is not available. Check the provided credentials and IP.")
            else:
                # get open threat event model
                event_data = event_model()
                # map EDR event to open threat event
                map_values(event_data, event)
                # send the threat event
                response = epo_client.run(THREAT_EVENT_REMOTE_COMMAND, event=json.dumps(event_data))
                logging.info("Event sent: {0}".format(response))
                return response
    except Exception as e:
        logging.error("----An exception occurred----")
        logging.error(e)


def connect(config):
    return mcafee.client(config.host, config.port or "8443", config.username, config.password)


def get_machine_information(guid):
    return epo_client.run("system.find", searchText=guid, searchNameOnly="false")


def event_model():
    with open(os.path.join(os.path.dirname(__file__), 'event.json')) as data_file:
        data = json.load(data_file)

    return data


def parse_detection_tags(event):
    return '.'.join(event["threat"]["detectionTags"])


def map_values(event_data, event):
    # this method will map values got from the threat event in EDR to the Open Threat Event Model

    event_data["event"]["entity"]["id"] = event["threat"]["maGuid"]

    event_data["event"]["_receivedUTC"] = event["timestamp"]
    event_data["event"]["threatName"] = event["threat"]["threatAttrs"]["name"]
    event_data["event"]["eventDesc"] = parse_detection_tags(event)

    event_data["event"]["target"]["fileName"] = event["threat"]["threatAttrs"]["path"]
    event_data["event"]["target"]["processName"] = event["threat"]["threatAttrs"]["name"]

    event_data["event"]["analyzer"]["detectedUTC"] = event["timestamp"]

    event_data["event"]["files"][0]["name"] = event["threat"]["threatAttrs"]["name"]
    event_data["event"]["files"][0]["hash"]["SHA-256"] = event["threat"]["threatAttrs"]["sha256"]
    event_data["event"]["files"][0]["hash"]["MD5"] = event["threat"]["threatAttrs"]["md5"]

    # machine information
    machine_information = get_machine_information(event["threat"]["maGuid"])

    if machine_information and len(machine_information) == 1:
        event_data["event"]["entity"]["osPlatform"] = machine_information[0]["EPOComputerProperties.OSPlatform"]
        event_data["event"]["entity"]["osType"] = machine_information[0]["EPOComputerProperties.OSType"]

        event_data["event"]["analyzer"]["hostName"] = machine_information[0]["EPOComputerProperties.ComputerName"]
        event_data["event"]["analyzer"]["ipv4"] = machine_information[0]["EPOComputerProperties.IPAddress"]
        event_data["event"]["analyzer"]["ipv6"] = machine_information[0]["EPOComputerProperties.IPV6"]
        event_data["event"]["analyzer"]["mac"] = machine_information[0]["EPOComputerProperties.NetAddress"]

        event_data["event"]["source"]["hostName"] = machine_information[0]["EPOComputerProperties.ComputerName"]
        event_data["event"]["source"]["ipv4"] = machine_information[0]["EPOComputerProperties.IPAddress"]
        event_data["event"]["source"]["ipv6"] = machine_information[0]["EPOComputerProperties.IPV6"]
        event_data["event"]["source"]["userName"] = machine_information[0]["EPOComputerProperties.UserName"]
        event_data["event"]["source"]["mac"] = machine_information[0]["EPOComputerProperties.NetAddress"]

        event_data["event"]["target"]["hostName"] = machine_information[0]["EPOComputerProperties.ComputerName"]
        event_data["event"]["target"]["ipv4"] = machine_information[0]["EPOComputerProperties.IPAddress"]
        event_data["event"]["target"]["ipv6"] = machine_information[0]["EPOComputerProperties.IPV6"]
        event_data["event"]["target"]["userName"] = machine_information[0]["EPOComputerProperties.UserName"]
        event_data["event"]["target"]["mac"] = machine_information[0]["EPOComputerProperties.NetAddress"]
