# -*- coding: utf-8 -*-
import functools
import json

from django.http import HttpResponse

from common.log import logger


class TryException(object):
    """
    decorator. log exception if task_definition has
    """

    def __init__(self, exception_desc='error', exception_return='', is_response=True, log=True):
        self.exception_desc = exception_desc
        self.exception_return = exception_return
        self.is_log = log
        self.is_response = is_response

    def __call__(self, task_definition):
        @functools.wraps(task_definition)
        def wrapper(*args, **kwargs):
            try:
                return task_definition(*args, **kwargs)
            # except timeout.TimeoutError:
            #     raise
            except Exception as e:
                desc = '[{0}] {1}'.format(task_definition.func_name, self.exception_desc)
                if self.is_log:
                    logger.exception(u"%s: %s", desc, e)
                else:
                    logger.warning(u"%s: %s", desc, e)
                message = u'系统异常,请联系管理员!{0}'.format(e.message) if not self.exception_desc else u"{0}异常".format(self.exception_desc)
                if self.is_response:
                    return HttpResponse(json.dumps({
                        'result': False,
                        'message': message,
                        'data': self.exception_return
                    }))
                return {"result": False, 'message': message, 'data': self.exception_return}

        return wrapper


def log_request_params(func):
    """视图函数参数记录装饰器"""

    def wrapper(request, *args, **kwargs):
        if request.method == "GET":
            logger.debug("request method: GET, params: \n %s" % request.GET)
        elif request.method == "POST":
            logger.debug("request method: POST, params: \n %s" % request.body)
        return func(request, *args, **kwargs)

    return wrapper
