
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
