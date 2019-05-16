"""Example of subscription to individual case-related events
"""
import logging
from mcafee_investigator_events import subscribe


@subscribe(entity='case', subtype='creation')
def case_created(event):
    logging.info("CASE CREATED: %s", event)


@subscribe(entity='case', subtype='priority-update')
def case_updated(event):
    logging.info("CASE PRIORITY UPDATED: %s", event)


@subscribe(entity='case', subtype='status-update')
def case_status_updated(event):
    logging.info("CASE STATUS UPDATED: %s", event)
