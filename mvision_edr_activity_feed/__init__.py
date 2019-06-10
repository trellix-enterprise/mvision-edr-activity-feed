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
import inspect
import jmespath
import sys
import json

__version__ = "0.0.5"


subscriptions = []


class CustomFunctions(jmespath.functions.Functions):
    @jmespath.functions.signature({'types': ['string']})
    def _func_lower(self, s):
        return s.lower()


options = jmespath.Options(custom_functions=CustomFunctions())


def subscribe(*args, **kwargs):
    entity = kwargs.get('entity')
    logging.debug("... Subscribe in place - entity: %s", entity)   
    subtype = kwargs.get('subtype')
    expression = args[0] if len(args) else None
    if not entity and not expression or len(args) > 1:
        raise TypeError("subscribe() expects a single positional "
                        "argument with a JSON path expression, or at least "
                        "an 'entity' keyword argument")
    entity = entity.lower() if entity else None
    subtype = subtype.lower() if subtype else None

    if not expression:
        if entity and subtype:
            expression = "lower(entity) == '{}' && lower(type) == '{}'".format(
                entity, subtype)
        else:
            expression = "lower(entity) == '{}'".format(entity)

    def decorator(func):
        # This decorator just returns the original function after adding it
        # to the list of subscriptions for the selected events

        import jmespath

        global subscriptions
        subscriptions.append((jmespath.compile(expression), func))

        return func

    return decorator


def reset_subscriptions():
    del subscriptions[:]

def getfullargs_internal(callback):
    logging.info("Major version info: %s", sys.version_info[0])
    if (sys.version_info[0] >= 3):
        return inspect.getfullargspec(callback).args
    else:
        logging.info("Lowest python version in use")
        return inspect.getargspec(callback).args

def invoke(payloads, configs, reraise=False):
    total_success = 0
    total_error = 0
    for payload in payloads:
        logging.debug('About to dispatch payload ...')
        try:
            # Enable the following code in case of global SysLogHandler solution:
            #logging.info(json.dumps(payload))
            # Disable the following code in case of global SysLogHandler solution:
            logging.debug("... Dispatching: %s", payload)
        except Exception:
            logging.error('Error while dumping payload to dispatch')

        callbacks = set()
        for expression, func in subscriptions:
            if expression.search(payload, options=options):
                callbacks.add(func)

        for callback in callbacks:
            try:
                if len(getfullargs_internal(callback)) == 2:
                    logging.debug('Calling subscription with configuration ...')
                    callback(payload, configs)
                else:
                    logging.debug('Calling subscription without configuration ...')
                    callback(payload)
                total_success += 1
            except Exception as exp:
                total_error += 1
                logging.error(
                    "Exception while executing callback: %s", exp)
                if reraise:
                    raise exp
    return (total_success, total_error)
