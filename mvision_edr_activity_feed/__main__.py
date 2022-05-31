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

import sys
import getpass
import argparse
from logging.handlers import SysLogHandler
import logging
import json
import os
from dxlstreamingclient.channel import Channel, ChannelAuth, ClientCredentialsChannelAuth
from mvision_edr_activity_feed import invoke, __version__ as version



def setup_argument_parser():
    parser = argparse.ArgumentParser(
        prog="mvision-edr-activity-feed",
        add_help=True,
        description="MVISION EDR Event Dispatcher CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--version',
                        action='version',
                        version=version)
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
    parser.add_argument('--module', required=True, action='append',
                        help="Module to register events")
    parser.add_argument('--period', '--wait', default=5, type=int,
                        help="Time (in seconds) between queries to the "
                             "event API")
    parser.add_argument('--topic', required=False, action='append',
                        type=str, help="Topic to subscribe to",
                        default=['case-mgmt-events', 'BusinessEvents', 'threatEvents'])
    parser.add_argument('--loglevel', default='info',
                        choices=['critical', 'error', 'warning',
                                 'info', 'debug', 'notset'])
    parser.add_argument('--logfile', type=argparse.FileType('w'),
                        default=sys.stdout)
    parser.add_argument('--consumer-reset', '--reset', action='store_true',
                        help="Starts the consumer group from the earliest "
                             "event available. This only works when "
                             "initializing the consumer group the first time")
    parser.add_argument('--consumer-group',
                        default='mvisionedr_events',
                        help="Name for the consumer group to use")
    parser.add_argument('--consumer-timeout',
                        default=300000, type=int,
                        help="Time (in seconds) before the consumer is "
                             "dropped by the Kafka backend. If event "
                             "processing takes longer than this, then events "
                             "might be duplicated.")
    parser.add_argument('--cert-bundle', type=str, default='',
                        required=False,
                        help='Path to a CA bundle file containing certificates of trusted CAs.')
    parser.add_argument('--config', required=False, action='append',
                        help="Configuration key/value pairs for callbacks")
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

    period = args.period
    loglevel = args.loglevel

    logging.basicConfig(level=getattr(logging, loglevel.upper(), None),
                        stream=args.logfile)
    
    logger = logging.getLogger()
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    sys.path.append(os.getcwd())
    # load modules containing subscriptions
    for module in args.module:
        try:

            __import__(module)
        except Exception as exp:
            logging.critical("While attempting to load module '%s': %s",
                             module, exp)
            exit(1)

    configs = get_config(args)

    CHANNEL_SCOPE = "soc.hts.c soc.hts.r soc.rts.c soc.rts.r soc.qry.pr soc.skr.pr soc.evt.vi soc.cop.r dxls.evt.w dxls.evt.r"
    CHANNEL_GRANT_TYPE = "client_credentials"
    CHANNEL_AUDIENCE = "mcafee"
    CHANNEL_IAM_URL = 'https://iam.mcafee-cloud.com/'
    if args.preprod:
        CHANNEL_IAM_URL = 'https://preprod.iam.mcafee-cloud.com/'

    logging.info("Consumer Group={a}".format(a=args.consumer_group))
    logging.info("Topics={a}".format(a=args.topic))

    logging.info("Starting event loop...")

    try:
        if args.username:
            with Channel(args.url,
                         auth=ChannelAuth(args.url,
                                          args.username,
                                          args.password,
                                          verify_cert_bundle=args.cert_bundle),
                         consumer_group=args.consumer_group,
                         verify_cert_bundle=args.cert_bundle,
                         offset='latest' if not args.consumer_reset else
                          'earliest') as channel:

                def process_callback(payloads):
                    logging.debug("Received payloads: \n%s",
                                  json.dumps(payloads, indent=4, sort_keys=True))
                    invoke(payloads, configs)
                    return True

                # Consume records indefinitely
                channel.run(process_callback, wait_between_queries=period, topics=args.topic)

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
                         verify_cert_bundle=args.cert_bundle,
                         offset='latest' if not args.consumer_reset else
                          'earliest') as channel:

                def process_callback(payloads):
                    logging.debug("Received payloads: \n%s",
                                  json.dumps(payloads, indent=4, sort_keys=True))
                    invoke(payloads, configs)
                    return True

                # Consume records indefinitely
                channel.run(process_callback, wait_between_queries=period, topics=args.topic)


    except Exception as e:
        logging.error("Unexpected error: {}".format(e))

if __name__ == "__main__":
    sys.exit(main())
