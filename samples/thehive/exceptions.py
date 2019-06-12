#!/usr/bin/python
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

log = logging.getLogger(__name__)


class TheHiveApiError(Exception):

    def __init__(self, status_code, description, msg=None):
        if msg is None:
            msg = "TheHiveAPIError: status_code '{}' description '{}'".format(
                status_code, description)
        super(TheHiveApiError, self).__init__(status_code, description, msg)
        self.status_code = status_code
        self.description = description
        self.msg = msg
