"""Example of subscription to individual case-related events
"""
import logging
from samples.slack import SlackEvents
from mvisionedractivityfeed import subscribe


slack_events = None


def setup(config):
    """Setup global connection to The hive using callback configuration
    parameters:
    * slack_token: Slack token
    * bot_user: User used by this script to post messages in Slack
    * default_user: Default user to invite to channels when no mapping is found
    * activity_channel: Channel in which to post summary
    * ui_url: URL of the Investigator UI
    """
    global slack_events
    if not slack_events:
        slack_events = SlackEvents(config.slack_token, config.ui_url,
                                   config.bot_user, config.activity_channel,
                                   lambda user: config.default_user)


@subscribe(entity='case', subtype='creation')
def case_created(event, config):
    logging.info("CASE CREATED: %s", event)
    setup(config)
    slack_events.case_created(event)


@subscribe(entity='case', subtype='priority-update')
def case_updated(event, config):
    logging.info("CASE PRIORITY UPDATED: %s", event)
    setup(config)
    slack_events.case_priority_updated(event)


@subscribe(entity='case', subtype='status-update')
def case_status_updated(event, config):
    logging.info("CASE STATUS UPDATED: %s", event)
    setup(config)
    slack_events.case_status_updated(event)


@subscribe(entity='case', subtype='select')
def case_select(event, config):
    logging.info("CASE SELECT: %s", event)
    setup(config)
    slack_events.case_selected_ui(event)


@subscribe(entity='case', subtype='unselect')
def case_unselect(event, config):
    logging.info("CASE UNSELECT: %s", event)
    setup(config)
    slack_events.case_unselected_ui(event)
