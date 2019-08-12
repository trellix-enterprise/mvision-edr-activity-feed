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
import hashlib
from datetime import datetime
from unittest import TestCase

from mock import mock, Mock

from epo.mcafeeepo import threat_event


class test_mcafeeepo(TestCase):

    @mock.patch('epo.mcafee.client', autospec=True)
    def test_threat_event(self, mock_client):

        # noinspection PyUnusedLocal
        def run_mock(*args, **kwargs):
            if args[0] == "system.find":
                return [{"EPOComputerProperties.OSPlatform": "Server",
                         "EPOComputerProperties.ComputerName": "WIN-CVH3N99HB3I",
                         "EPOComputerProperties.UserName": "Administrator",
                         "EPOComputerProperties.IPAddress": "172.31.0.34",
                         "EPOComputerProperties.NetAddress": "0.0.0.0",
                         "EPOComputerProperties.IPV6": "0:0:0:0:0:A00A:AC1F:22",
                         "EPOComputerProperties.OSType": "Windows 2008 R2"
                         }]
            elif args[0] == "DxlBrokerMgmt.createEpoThreatEvent":
                return "OK!"
            else:
                raise AssertionError("Unexpected call")

        mock_client.return_value.run = Mock(side_effect=run_mock)

        event = {
            "timestamp": "{0}".format(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            "threat": {
                "maGuid": "7F3C8734-5E96-4452-9D05-561E5A460B5B",
                "score": 80,
                "threatAttrs": {
                    "name": "test.exe",
                    "path": "\\test\\test.exe",
                    "md5": hashlib.md5("test").hexdigest(),
                    "sha256": hashlib.md5("test").hexdigest()
                },
                "detectionTags": {"tag1", "tag2"}
            }
        }

        response = threat_event(event=event, config=Mock(autospec=True))

        assert "OK!" == response

        mock_client.assert_called_once()
        assert 2 == mock_client.return_value.run.call_count
