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

import logging
from slackclient import SlackClient


status_mapping = {
    "new": "New",
    "in_progress": "In Progress",
    "incident_declared": "Incident Declared",
    "inconclusive": "Inconclusive",
    "dismissed": "Dismissed"
}

priority_mapping = {
    "medium": "Medium",
    "low": "Low",
    "high": "High",
    "unspecified": "Unspecified"
}

color_mapping = {
    "medium": "#ff8c00",
    "low": "#FFD700",  # gold
    "high": "#FF0000",  # red
    "unspecified": "#d3d3d3",
    "info": "#439FE0"
}


class SlackEvents(object):

    def __init__(self, slack_token, ui_url, bot_user, activity_channel,
                 map_user):
        self.sc = SlackClient(slack_token)
        self.ui_url = ui_url
        self.bot_user = bot_user
        self.activity_channel = activity_channel
        self.map_user = map_user
        self.channel_template = "mi-{}"

    def get_channel_name(self, case_id):
        return self.channel_template.format(case_id)[:21]

    def lookup_slack_channel_id(self, channel_name):
        # TODO: conditional caching based on output
        response = self.sc.api_call(
            "channels.list"
        )

        if not response['ok']:
            raise Exception(
                "Error while looking up channel ID: {}".format(response))

        for channel in response['channels']:
            if channel['name'] == channel_name:
                return channel['id']

        return None

    def lookup_slack_user_id(self, username):
        # TODO: conditional caching based on output
        response = self.sc.api_call(
            "users.list"
        )

        if not response['ok']:
            raise Exception(
                "Error while looking up user ID: {}".format(response))

        for member in response['members']:
            if member['name'] == username:
                return member['id']

        return None

    def get_case_url(self, case_id):
        url_template = "{}/#/cases/{{}}".format(self.ui_url)
        return url_template.format(case_id)

    def case_created(self, event):
        response = self.sc.api_call(
            "channels.create",
            name=self.get_channel_name(event['case']['id'])
        )

        if not response['ok']:
            logging.critical("Error while creating channel: %s", response)
            return

        normalized_name = response['channel']['name_normalized']
        channel_id = response['channel']['id']
        logging.info("Created channel '%s' in Slack", normalized_name)

        # Set channel purpose
        response = self.sc.api_call(
            "channels.setPurpose",
            channel=channel_id,
            purpose="Workspace for McAfee Investigator case '{}'. "
                    "Events related to this case will be posted here. ".format(
                        event['case']['name'])
        )
        if not response['ok']:
            logging.warning("Unable to set channel purpose: %s", response)

        slack_username = self.map_user(event['user'])
        slack_user_id = self.lookup_slack_user_id(slack_username)
        if slack_user_id:
            response = self.sc.api_call(
                "channels.invite",
                channel=channel_id,
                user=slack_user_id
            )
            if not response['ok']:
                logging.warning(
                    "Unable to invite user to channel: %s", response)
        else:
            logging.warning("User with handle '%s' not found", slack_username)

        response = self.sc.api_call(
            "chat.postMessage",
            channel=channel_id,
            as_user=False,
            link_names=True,
            parse="full",
            username=self.bot_user,
            attachments=[
                {
                    "title": "Case information",
                    "fallback": "Case URL: {}".format(
                        self.get_case_url(event['case']['id'])),
                    "fields": [
                        {
                            "title": "Name",
                            "value": event['case']['name']
                        },
                        {
                            "title": "ID",
                            "value": event['case']['id']
                        },
                        {
                            "title": "Reported by",
                            "value": event['user']
                        },
                    ],
                    "actions": [
                        {
                            "type": "button",
                            "text": "Open in McAfee Investigator",
                            "url": self.get_case_url(event['case']['id'])
                        }
                    ]
                }
            ]
        )
        if not response['ok']:
            logging.warning("Unable to post basic case information: %s",
                            response)

        # Mention the new case on the general channel
        activity_channel_id = self.lookup_slack_channel_id(
            self.activity_channel)
        if not activity_channel_id:
            logging.warning("Channel with name '%s' not found",
                            self.activity_channel)
            return

        response = self.sc.api_call(
            "chat.postMessage",
            channel=activity_channel_id,
            as_user=False,
            link_names=True,
            parse="full",
            username=self.bot_user,
            text="New channel #{} created for McAfee Investigator case `{}`. "
                 "@{} has been invited to join it".format(
                     normalized_name, event['case']['name'], slack_username)
        )

        if not response['ok']:
            logging.warning(
                "Unable to mention case creation on general channel: %s",
                response)

    def case_priority_updated(self, event):
        channel_id = self.lookup_slack_channel_id(
            self.get_channel_name(event['case']['id']))
        if not channel_id:
            logging.warning(
                "Channel with name '%s' not found", event['case']['id'])
            return

        response = self.sc.api_call(
            "chat.postMessage",
            channel=channel_id,
            as_user=False,
            link_names=True,
            parse="full",
            username=self.bot_user,
            attachments=[
                {
                    'title': "Priority update",
                    'text': priority_mapping[event['case']['priority']],
                    'color': color_mapping[event['case']['priority']]
                }
            ]
        )
        if not response['ok']:
            logging.warning("Unable to post priority update: %s", response)

    def case_status_updated(self, event):
        channel_id = self.lookup_slack_channel_id(
            self.get_channel_name(event['case']['id']))
        if not channel_id:
            logging.warning(
                "Channel with name '%s' not found", event['case']['id'])
            return

        response = self.sc.api_call(
            "chat.postMessage",
            channel=channel_id,
            as_user=False,
            link_names=True,
            parse="full",
            username=self.bot_user,
            attachments=[
                {
                    'title': "Status update",
                    'text': status_mapping[event['case']['status']],
                    'color': color_mapping['info']
                }
            ]
        )
        if not response['ok']:
            logging.warning("Unable to post status update: %s", response)

    def case_selected_ui(self, event):
        """A user started looking at a case in the UI
        """
        channel_id = self.lookup_slack_channel_id(
            self.get_channel_name(event['case']['id']))
        if not channel_id:
            logging.warning("Channel with name '%s' not found",
                            event['case']['id'])
            return

        response = self.sc.api_call(
            "chat.postMessage",
            channel=channel_id,
            as_user=False,
            link_names=True,
            parse="full",
            username=self.bot_user,
            attachments=[
                {
                    'title': "Time spent in case",
                    'text': 'User {} is currently looking at this case'.format(
                        event['user']),
                    'color': color_mapping['info']
                }
            ]
        )
        if not response['ok']:
            logging.warning("Unable to post status update: %s", response)

    def case_unselected_ui(self, event):
        """A user stopped looking at a case in the UI
        """
        channel_id = self.lookup_slack_channel_id(
            self.get_channel_name(event['case']['id']))
        if not channel_id:
            logging.warning(
                "Channel with name '%s' not found", event['case']['id'])
            return

        def map_time(seconds):
            return "{} seconds".format(seconds)

        response = self.sc.api_call(
            "chat.postMessage",
            channel=channel_id,
            as_user=False,
            link_names=True,
            parse="full",
            username=self.bot_user,
            attachments=[
                {
                    'title': "Time spent in case",
                    'text': 'User {} spent {} in this case'.format(
                        event['user'],
                        map_time(
                            event['case']
                            ['investigation-time']['elapsed-time'])),
                    'color': color_mapping['info']
                }
            ]
        )
        if not response['ok']:
            logging.warning("Unable to post status update: %s", response)
