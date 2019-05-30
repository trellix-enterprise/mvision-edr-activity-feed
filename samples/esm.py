"""
Example of subscription to individual case-related events
"""
import logging
from mvision_edr_activity_feed import subscribe
from samples.esm import EsmEvents

esm_events = None

def setup(config):
    global esm_events
    if not esm_events:
        esm_events = EsmEvents(config.url)

@subscribe(entity='case')
def case_created(event, config):
    logging.info("CASE CREATED: {}".format(event))
    setup(config)
    esm_events.case_created(event)

@subscribe(entity='threat')
def case_created(event, config):
    logging.info("THREAT CREATED: {}".format(event))
    setup(config)
    esm_events.threat_created(event)