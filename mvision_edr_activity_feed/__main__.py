import sys
import argparse
import logging
import json
import os
from dxlstreamingclient.channel import Channel, ChannelAuth
from mvision_edr_activity_feed import __version__ as version


INTERRUPTED = False


def setup_argument_parser():
    parser = argparse.ArgumentParser(
        prog="mvision-edr-activity-feed",
        add_help=True,
        description="MVISION EDR Activity Feed",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--version',
                        action='version',
                        version=version)
    parser.add_argument('--url', required=True,
                        help="Base URL for McAfee Investigator")
    parser.add_argument('--username', required=True,
                        help="Username for the service")
    parser.add_argument('--password', required=True,
                        help="Password for the service")
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

    period = args.period
    loglevel = args.loglevel

    logging.basicConfig(level=getattr(logging, loglevel.upper(), None),
                        stream=args.logfile)

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

    logging.info("Sarting event loop...")

    while not INTERRUPTED:
        try:
            with Channel(args.url,
                         auth=ChannelAuth(args.url,
                                          args.username,
                                          args.password,
                                          verify_cert_bundle=args.cert_bundle),
                         consumer_group=args.consumer_group,
                         verify_cert_bundle=args.cert_bundle) as channel:

                def process_callback(payloads):
                    print("Received payloads: \n%s",
                          json.dumps(payloads, indent=4, sort_keys=True))

                channel.run(process_callback, wait_between_queries=period, topics=args.topic)


        except Exception as e:
            logging.error("Unexpected error: {}".format(e))

if __name__ == "__main__":
    sys.exit(main())
