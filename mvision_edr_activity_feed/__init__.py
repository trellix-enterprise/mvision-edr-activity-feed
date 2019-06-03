import logging
import inspect
import jmespath
import sys

__version__ = "0.0.5"


subscriptions = []


class CustomFunctions(jmespath.functions.Functions):
    @jmespath.functions.signature({'types': ['string']})
    def _func_lower(self, s):
        return s.lower()


options = jmespath.Options(custom_functions=CustomFunctions())


def subscribe(*args, **kwargs):
    # entity=None, subtype=None, expression=None
    entity = kwargs.get('entity')
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
    if (sys.version_info > (2, 7)):
        return inspect.getfullargspec(callback).args
    else:
        return inspect.getargspec(callback).args

def invoke(payloads, configs, reraise=False):
    total_success = 0
    total_error = 0
    for payload in payloads:
        logging.debug("Dispatching: %s", payload)

        callbacks = set()
        for expression, func in subscriptions:
            if expression.search(payload, options=options):
                callbacks.add(func)

        for callback in callbacks:
            try:
                if len(getfullargs_internal(callback)) == 2:
                    callback(payload, configs)
                else:
                    # calling subscription without configuration
                    callback(payload)
                total_success += 1
            except Exception as exp:
                total_error += 1
                logging.error(
                    "Exception while executing callback: %s", exp)
                if reraise:
                    raise exp
    return (total_success, total_error)
