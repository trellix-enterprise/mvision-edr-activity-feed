import unittest
import jmespath
from mock import MagicMock
from mvision_edr_activity_feed import subscribe, invoke, reset_subscriptions


class Test(unittest.TestCase):
    def setUp(self):
        pass

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

if __name__ == '__main__':
    unittest.main()