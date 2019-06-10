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

import unittest
import jmespath
import base64
import json
from mock import patch, MagicMock
from mvision_edr_activity_feed import subscribe, invoke, reset_subscriptions
from mvision_edr_activity_feed.__main__ import get_config, setup_argument_parser
from dxlstreamingclient.channel import Channel, ChannelAuth

INTERRUPTED = False

class Test(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost"
        self.username = "someone"
        self.password = "password"
        self.consumer_group = "a_consumer_group"
        self.verify_cert_bundle = ""
        self.topic = "foo-topic"
        self.period = 4

    def tearDown(self):
        pass

    def test_subscription(self):

        reset_subscriptions()

        self.one_param_count = 0
        self.two_param_count = 0
        self.tenant_sub_count = 0
        self.priority_sub_count = 0

        def one_param(event):
            self.assertEqual('case', event['entity'].lower())
            self.one_param_count += 1

        def two_param(event, config):
            self.assertEqual('case', event['entity'].lower())
            self.assertEqual('creation', event['type'].lower())
            self.assertEqual(config.foo, 'bar')
            self.two_param_count += 1

        def tenant_sub(event):
            self.assertEqual('jmdacruz', event['user'])
            self.tenant_sub_count += 1

        def priority_sub(event):
            self.assertEqual('High', event['case']['priority'])
            self.priority_sub_count += 1

        subscribe(entity='casE')(one_param)
        subscribe(entity='case', subtype='creation')(two_param)
        subscribe("user == 'jmdacruz'")(tenant_sub)
        subscribe("case.priority == 'High'")(priority_sub)

        event = {
            "id": "a45a03de-5c3d-452a-8a37-f68be954e784",
            "entity": "CaSe",
            "type": "creaTion",
            "tenant-id": "7af4746a-63be-45d8-9fb5-5f58bf909c25",
            "user": "jmdacruz",
            "origin": "",
            "nature": "",
            "timestamp": "",
            "transaction-id": "",
            "case": {
                "id": "4e8e23f4-9fe9-4215-92c9-12c9672be9f1",
                "name": "A great case full of malware",
                "url": "https://ui-int-cop.soc.mcafee.com/#/"
                       "cases/4e8e23f4-9fe9-4215-92c9-12c9672be9f1",
                "priority": "Low"
            }
        }

        config = MagicMock()
        config.foo = 'bar'

        s, e = invoke([event], config, reraise=True)
        self.assertEqual(s, 3)
        self.assertEqual(e, 0)
        self.assertEqual(self.one_param_count, 1)
        self.assertEqual(self.two_param_count, 1)
        self.assertEqual(self.tenant_sub_count, 1)
        self.assertEqual(self.priority_sub_count, 0)

    def test_subscription_errors(self):

        reset_subscriptions()

        def one_param(event):
            pass

        with self.assertRaises(TypeError):
            subscribe()(one_param)

        with self.assertRaises(TypeError):
            subscribe(subtype="foo")(one_param)

        with self.assertRaises(TypeError):
            subscribe("A", "B")(one_param)

        with self.assertRaises(jmespath.exceptions.ParseError):
            subscribe("&&&")(one_param)

    def test_invocation_errors(self):

        reset_subscriptions()

        class CustomException(Exception):
            pass

        def one_param(event):
            raise CustomException()

        subscribe(entity='finding')(one_param)

        event = {
            "id": "a45a03de-5c3d-452a-8a37-f68be954e784",
            "entity": "finding",
            "type": "new",
            "tenant-id": "7af4746a-63be-45d8-9fb5-5f58bf909c25",
            "user": "jmdacruz",
            "origin": "",
            "nature": "",
            "timestamp": "",
            "transaction-id": "",
            "case": {
                "id": "4e8e23f4-9fe9-4215-92c9-12c9672be9f1",
                "name": "A great case full of malware",
                "url": "https://ui-int-cop.soc.mcafee.com/#/"
                       "cases/4e8e23f4-9fe9-4215-92c9-12c9672be9f1",
                "priority": "Low"
            }
        }

        config = MagicMock()
        config.foo = 'bar'

        with self.assertRaises(CustomException):
            s, e = invoke([event], config, reraise=True)
            self.assertEqual(s, 1)
            self.assertEqual(e, 0)

    def test_unregistered_event(self):

        reset_subscriptions()

        event = {
            "id": "a45a03de-5c3d-452a-8a37-f68be954e784",
            "entity": "foo",
            "type": "bar",
            "tenant-id": "7af4746a-63be-45d8-9fb5-5f58bf909c25",
            "user": "jmdacruz",
            "origin": "",
            "nature": "",
            "timestamp": "",
            "transaction-id": "",
            "case": {
                "id": "4e8e23f4-9fe9-4215-92c9-12c9672be9f1",
                "name": "A great case full of malware",
                "url": "https://ui-int-cop.soc.mcafee.com/#/"
                       "cases/4e8e23f4-9fe9-4215-92c9-12c9672be9f1",
                "priority": "Low"
            }
        }

        config = MagicMock()
        config.foo = 'bar'

        s, e = invoke([event], config, reraise=True)
        self.assertEqual(s, 0)
        self.assertEqual(e, 0)

    def test_authentication(self):
        pass

    def test_channel(self):
        pass
    
    def test_get_config(self):
        class Arguments(new_cfg):
            config = new_cfg
        ars = Arguments(["key1=value1","key2=value2","key3=value3"])
        cfg = get_config(ars)
        self.assertEqual(cfg["key1"], "value1")
        self.assertEqual(cfg["key2"], "value2")
        self.assertEqual(cfg["key3"], "value3")
        
    def test_setup_argument_parser(self):
        p = setup_argument_parser()
        self.assertIsNotNone(p)
        #ars = this_parser.parse_args()
        #cfg = get_config(ars)
        #self.assertIsNotNone(cfg)

"""
    # CS commented all this code on purpose (TODO: Ask MDC why):
    def test_main(self):
        case_event = {
            "id": "a45a03de-5c3d-452a-8a37-f68be954e784",
            "entity": "case",
            "type": "creation",
            "tenant-id": "7af4746a-63be-45d8-9fb5-5f58bf909c25",
            "user": "jmdacruz",
            "origin": "",
            "nature": "",
            "timestamp": "",
            "transaction-id": "",
            "case":
                {
                    "id": "c00547df-6d74-4833-95ad-3a377c7274a6",
                    "name": "A great case full of malware",
                    "url": "https://ui-int-cop.soc.mcafee.com/#/cases"
                           "/4e8e23f4-9fe9-4215-92c9-12c9672be9f1",
                    "priority": "Low"
                }
        }
   
        encoded_event = base64.b64encode(bytes(json.dumps(case_event), 'utf-8'))
   
        with patch('requests.Session') as session:
            session.return_value = MagicMock()  # self.request
            session.return_value.post = MagicMock()
            session.return_value.get = MagicMock()
            session.return_value.delete = MagicMock()
   
            create_mock = MagicMock()
            create_mock.status_code = 200
            create_mock.json = MagicMock(
                return_value={'consumerInstanceId': 1234})
   
            subscr_mock = MagicMock()
            subscr_mock.status_code = 204
   
            consum_mock = MagicMock()
            consum_mock.status_code = 200
            consum_mock.json = MagicMock(
                return_value={'records': [
                    {
                        'routingData': {
                            'topic': 'foo-topic'
                        },
                        'message': {
                            'payload': encoded_event
                        },
                        'partition': 1,
                        'offset': 1
                    }
                ]})
   
            # commit_consumer_error_mock = MagicMock()
            # commit_consumer_error_mock.status_code = 404
            # commit_error_mock = MagicMock()
            # commit_error_mock.status_code = 500
            run_mock = MagicMock()
            run_mock.status_code = 204
            # delete_mock = MagicMock()
            # delete_mock.status_code = 204
            # delete_404_mock = MagicMock()
            # delete_404_mock.status_code = 404
            # delete_500_mock = MagicMock()
            # delete_500_mock.status_code = 500
   
            session.return_value.post.explode.return_value = [
                create_mock, run_mock]
            #create_mock, subscr_mock, commit_consumer_error_mock,
            # commit_error_mock, run_mock]
            
            session.return_value.get.side_effect = [consum_mock]
            # session.return_value.delete.side_effect = [
            #     delete_500_mock, delete_404_mock, delete_mock]
   
            with Channel(self.url,
                         auth= ChannelAuth(self.url, self.username, self.password, verify_cert_bundle=self.verify_cert_bundle),
                         consumer_group=self.consumer_group,
                         verify_cert_bundle=self.verify_cert_bundle) as channel:        
        
                # def process_callback(payloads):
                #     print("Received payloads: \n%s",
                #           json.dumps(payloads, indent=4, sort_keys=True))
                #     self.assertEqual(payloads[0]['id'],
                #                      'a45a03de-5c3d-452a-8a37-f68be954e784')
   
                channel.run(json.dumps(case_event, indent=4, sort_keys=True), wait_between_queries=self.period, topics=self.topic)
   
            with self.assertRaises(ConsumerError):
                channel.commit()
            with self.assertRaises(TemporaryError):
                channel.commit()
   
            channel.commit()
   
            channel.unsubscribe()  # currently noop
   
            with self.assertRaises(TemporaryError):
                channel.delete()  # trigger 500
                session.return_value.delete.assert_called_with(
                    "http://localhost/databus/consumer-service/v1/consumers/1234")
                session.return_value.delete.reset_mock()
            
            channel.delete()  # trigger silent 404
            session.return_value.delete.assert_called_with(
            "http://localhost/databus/consumer-service/v1/consumers/1234")
            session.return_value.delete.reset_mock()
    
            channel.consumer_id = "1234"  # resetting consumer
            channel.delete()  # Proper deletion
            session.return_value.delete.assert_called_with(
                "http://localhost/databus/consumer-service/v1/consumers/1234")
            session.return_value.delete.reset_mock()
            
            channel.delete()  # trigger early exit
            INTERRUPTED = False  # re-enabling retry mechanism
"""

if __name__ == '__main__':
    unittest.main()
