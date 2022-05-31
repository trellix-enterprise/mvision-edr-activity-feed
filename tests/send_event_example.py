from __future__ import absolute_import
from __future__ import print_function
import base64
import json
import os
import sys
import logging
import argparse
from dxlstreamingclient.channel import Channel, ChannelAuth , ClientCredentialsChannelAuth



def setup_argument_parser():
    parser = argparse.ArgumentParser(
        prog="send-event-example",
        add_help=True,
        description="MVISION EDR Event Producer Example",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--url', required=True,
                        help="Base URL for MVISION EDR")
    parser.add_argument('--username', required=False,
                        help="MVISION EDR Username")
    parser.add_argument('--password', required=False,
                        help="MVISION EDR Password")
    parser.add_argument('--client_id', '-C',
                        required=False, type=str,
                        help='MVISION EDR Client ID')
    parser.add_argument('--client_secret', '-S',
                        required=False, type=str,
                        help='MVISION EDR Client Secret')
    parser.add_argument('--tenant_id', '-T',
                        required=True, type=str,
                        help='MVISION EDR Client Tenant ID')
    parser.add_argument('--topic', required=False,
                        type=str, help="Topic to subscribe to",
                        default='threatEvents')
    parser.add_argument('--consumer-group', required=False,
                        default='mvisionedr_events',
                        help="Name for the consumer group to use")
    parser.add_argument('--cert-bundle', type=str, default='',
                        required=False,
                        help='Path to a CA bundle file containing certificates of trusted CAs.')
    parser.add_argument('--preprod', '-PP',
                        required=False, action='store_true',
                        default=False, help='Option to generate the authentication token for the preprod environment.')
    return parser


def get_config(args):
    class Struct(object):
        pass
    configs = Struct()
    for config in args.config or []:
        k, v = config.split('=')
        configs.__dict__[k] = v
    return configs

def main():

    parser = setup_argument_parser()
    args = parser.parse_args()
    if args.username and args.client_id:
        logging.critical("Use only one of the authentication credentials, either username/password or client_id/client_secret")
        exit(1)
    if not args.username:
        if not args.client_id:
            logging.critical("Missing the authentication credentials. Use either username/password or client_id/client_secret")
            exit(1)
        if not args.client_secret:
            args.client_secret = getpass.getpass(prompt='MVISION EDR Client Secret: ')
    if not args.client_secret and not args.password:
        args.password = getpass.getpass(prompt='MVISION EDR Password: ')

    CHANNEL_SCOPE = "soc.hts.c soc.hts.r soc.rts.c soc.rts.r soc.qry.pr soc.skr.pr soc.evt.vi soc.cop.r dxls.evt.w dxls.evt.r"
    CHANNEL_GRANT_TYPE = "client_credentials"
    CHANNEL_AUDIENCE = "mcafee"
    CHANNEL_IAM_URL = 'https://iam.mcafee-cloud.com/'
    if args.preprod:
        CHANNEL_IAM_URL = 'https://preprod.iam.mcafee-cloud.com/'

    root_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(root_dir + "/../..")
    sys.path.append(root_dir + "/..")
    # Configure local logger
    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    # Create the message payload to be included in a record
    message_payload = {
        "message": "Hello from Activity Feed"
    }
    # Create the full payload with records to produce to the channel
    channel_payload = {
        "records": [
            {
                "routingData": {
                    "topic": args.topic + "-" + args.tenant_id,
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
    # Create a new channel object with username/password
    if args.username:
        with Channel(args.url,
            auth=ChannelAuth(args.url,
                args.username,
                args.password,
                verify_cert_bundle=args.cert_bundle),
            consumer_group=args.consumer_group,
            verify_cert_bundle=args.cert_bundle) as channel:
            # Produce the payload records to the channel
            channel.produce(channel_payload)

    # Create a new channel object with client_id/client_secret
    if args.client_id:
        with Channel(args.url,
            auth=ClientCredentialsChannelAuth(CHANNEL_IAM_URL,
                args.client_id,
                args.client_secret,
                verify_cert_bundle=args.cert_bundle,
                scope=CHANNEL_SCOPE,
                grant_type=CHANNEL_GRANT_TYPE,
                audience=CHANNEL_AUDIENCE),
            consumer_group=args.consumer_group,
            verify_cert_bundle=args.cert_bundle) as channel:
            # Produce the payload records to the channel
            channel.produce(channel_payload)

    print("Succeeded.")

if __name__ == "__main__":
    sys.exit(main())

#
#python send_event_example.py --url https://api-inteks.soc.mcafee.com --client_id=CLIENT_ID --client_secret=CLIENT_SECRET --tenant_id=TENANT_ID --preprod
#
#python mvision_edr_activity_feed --url https://api-inteks.soc.mcafee.com --client_id=CLIENT_ID --client_secret=CLIENT_SECRET --module samples.generic --loglevel debug --preprod
#
