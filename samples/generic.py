"""Example of subscription to all case-related events
"""
import logging
from mvision_edr_activity_feed import subscribe


@subscribe(entity='case')
def any_case_event(event):
    logging.info("GENERIC CASE EVENT: %s", event)


@subscribe("user == 'jmdacruz'")
def any_case_event_for_user(event):
    logging.info("GENERIC CASE EVENT FOR USER: %s", event)
