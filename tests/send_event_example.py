from __future__ import absolute_import
from __future__ import print_function
import base64
import json
import os
import sys
import logging
from dxlstreamingclient.channel import Channel, ChannelAuth , ClientCredentialsChannelAuth
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir + "/../..")
sys.path.append(root_dir + "/..")
# Configure local logger
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)
# Change these below to match the appropriate details for your
# channel connection.
CHANNEL_URL = "https://api-inteks.soc.mcafee.com"
CHANNEL_IAM_URL = "https://preprod.iam.mcafee-cloud.com/"
CHANNEL_CLIENT_ID = "CLIENT_ID"
CHANNEL_CLIENT_SECRET = "CLIENT_SECRET"
CHANNEL_CONSUMER_GROUP = "sample_consumer_group"
CHANNEL_TOPIC = "epo-xml-threatevents-50B7A3F9-49D0-44EF-B44B-E6723A097BD6"
CHANNEL_SCOPE = "soc.hts.c soc.hts.r soc.rts.c soc.rts.r soc.qry.pr soc.skr.pr soc.evt.vi soc.cop.r dxls.evt.w dxls.evt.r"
CHANNEL_GRANT_TYPE = "client_credentials"
CHANNEL_AUDIENCE = "mcafee"
# Path to a CA bundle file containing certificates of trusted CAs. The CA
# bundle is used to validate that the certificate of the server being connected
# to was signed by a valid authority. If set to an empty string, the server
# certificate is not validated.
VERIFY_CERTIFICATE_BUNDLE = ""
# Create the message payload to be included in a record
message_payload = {
    "message": "Hello from OpenDXL"
}
# Create the full payload with records to produce to the channel
channel_payload = {
    "records": [
        {
            "routingData": {
                "topic": CHANNEL_TOPIC,
                "shardingKey": ""
            },
            "message": {
                "headers": {},
                # Convert the message payload from a dictionary to a
                # base64-encoded string.
                "payload": base64.b64encode(
                    json.dumps(message_payload).encode()).decode()
            }
        }
    ]
}
# Create a new channel object
with Channel(CHANNEL_URL,
    auth=ClientCredentialsChannelAuth(CHANNEL_IAM_URL,
        CHANNEL_CLIENT_ID,
        CHANNEL_CLIENT_SECRET,
        verify_cert_bundle=VERIFY_CERTIFICATE_BUNDLE,
        scope=CHANNEL_SCOPE,
        grant_type=CHANNEL_GRANT_TYPE,
        audience=CHANNEL_AUDIENCE),
    consumer_group=CHANNEL_CONSUMER_GROUP,
    verify_cert_bundle=VERIFY_CERTIFICATE_BUNDLE,
    offset='earliest') as channel:
    # Produce the payload records to the channel
    channel.produce(channel_payload)
print("Succeeded.")
#
#python mvision_edr_activity_feed --url https://api-inteks.soc.mcafee.com --client_id=CLIENT_ID --client_secret=CLIENT_SECRET --module samples.generic --loglevel debug --preprod --topic epo-xml-threatevents
#
