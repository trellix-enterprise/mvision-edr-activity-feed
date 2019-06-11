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

from thehive4py.api import TheHiveApi
from thehive4py.exceptions import CaseException, CaseTaskException
import requests


class TheHiveApiWrapper(TheHiveApi):

    def update_case(self, case):
        """
        Update a case.
        :param case: The case to update. The case's `id` determines which case
        to update.
        :return:
        """
        req = self.url + "/api/case/{}".format(case.id)

        # Choose which attributes to send
        update_keys = [
            'title', 'description', 'severity', 'startDate', 'owner', 'flag',
            'tlp', 'tags', 'resolutionStatus', 'impactStatus', 'summary',
            'endDate', 'metrics', 'status'
        ]
        data = {k: v for k, v in case.__dict__.items() if k in update_keys}

        try:
            return requests.patch(req,
                                  headers={'Content-Type': 'application/json'},
                                  json=data, proxies=self.proxies,
                                  auth=self.auth, verify=self.cert)
        except requests.exceptions.RequestException as exp:
            raise CaseException("Case update error: {}".format(exp))

    def delete_case(self, case_id):

        req = self.url + "/api/case/{}".format(case_id)

        try:
            return requests.delete(req, proxies=self.proxies, auth=self.auth,
                                   verify=self.cert)
        except requests.exceptions.RequestException as e:
            raise CaseException("Case delete error: {}".format(e))

    def list_cases(self):

        req = self.url + "/api/case"

        try:
            return requests.get(req, proxies=self.proxies, auth=self.auth,
                                verify=self.cert)
        except requests.exceptions.RequestException as e:
            raise CaseException("Case list error: {}".format(e))

    def update_task(self, task_id, **attributes):

        req = self.url + "/api/case/task/" + task_id

        # Choose which attributes to send
        update_keys = [
            'title', 'description', 'startDate', 'owner', 'flag', 'endDate',
            'status', 'owner'
        ]
        data = {k: v for k, v in attributes.items() if k in update_keys}

        try:
            return requests.patch(req,
                                  headers={'Content-Type': 'application/json'},
                                  json=data, proxies=self.proxies,
                                  auth=self.auth, verify=self.cert)
        except requests.exceptions.RequestException as e:
            raise CaseTaskException("Task update error: {}".format(e))
