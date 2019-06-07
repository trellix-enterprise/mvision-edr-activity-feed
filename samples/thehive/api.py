# -*- coding: utf-8 -*-

"""
MCAFEE CONFIDENTIAL
copyright © 2017 McAfee LLC.
The source code contained or described herein and all documents related to
the source code ("Material") are owned by McAfee Corporation or its suppliers
or licensors. Title to the Material remains with McAfee Corporation or its
suppliers and licensors. The Material contains trade secrets and proprietary
and confidential information of McAfee or its suppliers and licensors. The
Material is protected by worldwide copyright and trade secret laws and
treaty provisions. No part of the Material may be used, copied, reproduced,
modified, published, uploaded, posted, transmitted, distributed, or
disclosed in any way without McAfee's prior express written permission.

No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be
express and approved by McAfee in writing.
"""

import logging
import json
import requests
import time

from thehive4py.models import Case
from thehive4py.query import String, Eq

from samples.thehive import (
    CaseCreationModel, case_tasks_log_model, case_observable_model)
from samples.thehive.exceptions import TheHiveApiError
from samples.thehive import (
    case_priority_mappings, case_status_mappings, case_resolution_mappings)
from samples.thehive import TheHiveApiWrapper
log = logging.getLogger(__name__)


class TheHiveApiClient(object):

    def __init__(self, tenant):
        self.tenant = tenant
        self.api = TheHiveApiWrapper(self.tenant.hive_api_url,
                                     self.tenant.hive_api_token)

    def get_case(self, id):
        response = self.api.get_case(id)
        if response.status_code == requests.codes.ok:
            log.info("Case {} successfully retrieved".format(id))
            log.debug(json.dumps(response.json(), indent=4, sort_keys=True))
            return response.json()
        else:
            raise TheHiveApiError(response.status_code, response.text)

    def create_case(self, event):
        case = CaseCreationModel(event, self.tenant).case
        response = self.api.create_case(case)
        if response.status_code == requests.codes.created:
            mi_caseid = event['case']['id']
            hive_caseid = response.json()['id']
            log.info("Case %s successfully created for Investigator case %s",
                     hive_caseid, mi_caseid)
            log.debug(json.dumps(response.json(), indent=4, sort_keys=True))

            return response.json()
        else:
            raise TheHiveApiError(response.status_code, response.text)

    def get_case_tasks(self, id, **filter):
        response = self.api.get_case_tasks(id, **filter)
        if response.status_code == requests.codes.ok:
            log.info("Tasks for case {} successfully retrieved".format(id))
            log.debug(json.dumps(response.json(), indent=4, sort_keys=True))
            return response.json()
        else:
            raise TheHiveApiError(response.status_code, response.text)

    def create_task_log(self, id, event):
        tasklog = case_tasks_log_model(event)
        response = self.api.create_task_log(id, tasklog)
        if response.status_code == requests.codes.created:
            log.info("Tasklog {} successfully created".format(
                response.json()['id']))
            log.debug(json.dumps(response.json(), indent=4, sort_keys=True))
            return response.json()
        else:
            raise TheHiveApiError(response.status_code, response.text)

    def update_case_priority(self, event):
        mi_caseid = event['case']['id']
        try:
            hive_caseid = self.get_hive_case_id(mi_caseid)
            response_dict = self.api.get_case(hive_caseid).json()
            print(json.dumps(response_dict, indent=4, sort_keys=True))
            new_severity = case_priority_mappings[
                event['case']['priority'].lower()]
            # updated_case = Case(**response_dict)
            updated_case = Case(severity=new_severity)
            keys_to_del = updated_case.__dict__
            print(keys_to_del)
            for key in keys_to_del.keys():
                delattr(updated_case, key)
            updated_case.severity = new_severity
            updated_case.id = hive_caseid
            response = self.api.update_case(updated_case)
            log.info("case updated status: {}".format(response.status_code))
            log.info("response body: {}".format(response.text))
            self.update_case_tasks(event)
        except Exception:
            log.error("An error occurred while updating a case : %s",
                      mi_caseid, exc_info=True)

    def _target_task(self, event):

        if event['nature'].lower() == "user".lower():
            return "user"
        else:
            if (event['entity'] == 'finding' or event['entity'] ==
                    'observable') and event['nature'] == 'system':
                return "analytics"
            else:
                return "system"

    def update_case_tasks(self, event):
        mi_caseid = event['case']['id']
        task_name = self._target_task(event)
        try:
            hive_caseid = self.get_hive_case_id(mi_caseid)
            response = self.get_case_tasks(hive_caseid,
                                           query=String(task_name))
            task_id = response[0]['id']
            if response[0]['status'] == 'Waiting':
                task_resp = self.api.update_task(
                    task_id,
                    **{'status': 'InProgress', 'owner': event['user']})
                log.info("task updated status: %s", task_resp.status_code)
                log.info("response body: %s", task_resp.text)
            return self.create_task_log(task_id, event)
        except Exception:
            log.error("case task update failed: %s", mi_caseid, exc_info=True)

    def update_case_status(self, event):
        mi_caseid = event['case']['id']
        try:
            hive_caseid = self.get_hive_case_id(mi_caseid)
            updated_case = Case()
            keys_to_del = updated_case.__dict__
            print(keys_to_del)
            for key in keys_to_del.keys():
                delattr(updated_case, key)

            updated_case.status = case_status_mappings[
                event['case']['status'].lower()]
            if updated_case.status != 'Resolved':
                pass
            else:
                updated_case.resolutionStatus = case_resolution_mappings[
                    event['case']['status'].lower()]
                updated_case.impactStatus = 'WithImpact'
                updated_case.id = hive_caseid
                response = self.api.update_case(updated_case)
                log.info("case updated status: %s", response.status_code)
                log.info("response body: %s", response.text)
            self.update_case_tasks(event)
        except Exception:
            log.error("An error occurred while updating a case : %s",
                      mi_caseid, exc_info=True)

    def create_observables(self, event):
        log.info("creating observables for the finding")
        try:
            observables_created = 0
            for observable in event['finding']['observables']:

                if (self.create_observable(observable).status_code
                        == requests.codes.created):
                    observables_created += 1

            if observables_created == len(event['finding']['observables']):
                self.update_case_tasks(event)

        except Exception:
            log.error("findings creation failed: %s",
                      event['finding']['id'], exc_info=True)

    def create_observable(self, event):
        mi_caseid = event['case']['id']
        try:
            hive_caseid = self.get_hive_case_id(mi_caseid)
            case_observable = case_observable_model(event)
            response = self.api.create_case_observable(
                hive_caseid, case_observable)
            if response.status_code == requests.codes.created:
                self.update_case_tasks(event)
            else:
                raise Exception("Observable creation failed ({}): {}"
                                .format(response.status_code, response.text))
            log.info("Observables saved: %s",
                     json.dumps(self.api.get_case_observables(
                         hive_caseid).json(), indent=4, sort_keys=True))
            return response
        except Exception:
            log.error("Observable creation failed for case: %s",
                      mi_caseid, exc_info=True)

    def get_hive_case_id(self, mi_caseid):
        """This function attempts to retrieve the case in The Hive using a tags
        to store the case ID from McAfee Investigator. A few considerations:

        * If this tag is removed, then this mapping will fail
        * The Hive uses Elasticsearch for storage, and using the default
          index refresh interval (1s). This code will retry for 5 seconds while
          no results are found.

        If this approach is not enough for accurately tracking case mapping,
        our recomendation is to setup some local storage and change this
        implementation. That said, this should work most of the time.
        """
        num_retries = 5
        time_between_retries = 1  # seconds
        while num_retries:
            try:
                response = self.api.find_cases(query=Eq('tags', mi_caseid))
                if response.status_code == requests.codes.ok:
                    return response.json()[0]['id']
            except Exception:
                log.warning(
                    "Exception during case lookup attempt #%s (will retry)",
                    num_retries, exc_info=True)
            time.sleep(time_between_retries)
            num_retries -= 1

        raise Exception(
            "Could not lookup case with ID '{}' in The Hive".format(mi_caseid))
