#-*- coding: utf-8 -*-
# Python 3.6

import os
import sys
import json
import requests
import logging

from .exc import *

log = logging.getLogger('qi.common.api.base')

HTTPS_PORT = 443

HSC_NO_CONTENT = 204
HSC_BAD_REQUEST = 400
HSC_NOT_FOUND = 404
HSC_ERROR = 500

def error_msg(err_msg, e, **kwargs):
    msg = "{} e={}, {}"
    return msg.format(err_msg, str(e), str(kwargs))

def conf_error_handle(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IOError as e:
            raise ConfigError(error_msg("ConfigFileError.", e))
        except ValueError as e:
            raise ConfigError(error_msg("ConfigValueError.", e))
        except KeyError as e:
            raise ConfigError(error_msg("ConfigKeyError.", e))
    return wrapper

def res_error_handle(func):
    def wrapper(*args, **kwargs):
        error_kwargs = {"resource":args[1], "params":args[2]}
        try:
            json_str = func(*args, **kwargs)
            return json_str
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(error_msg("ConnectionError.", e, 
                                  **error_kwargs))
        except ValueError as e:
            raise ResponseError(error_msg("ResponseError.", e, 
                                **error_kwargs))
    return wrapper

class APIBase(object):
    """ resta api server 호출 base class
    api response body 가 json 형식이 아닌 경우 예외 발생
    """
    def __init__(self):
        self.config = {
            "host":None,
            "port":None
        }
        self.def_req_kwargs = {
            "verify":False,
            "timeout":15
        }
        self.err_status_map ={
            HSC_NO_CONTENT:NoContent("No Content"),
            HSC_BAD_REQUEST:BadRequest("Bad Request"),
            HSC_NOT_FOUND:NotFound("Not Found"),
            HSC_ERROR:ServerError("Server Error"),
        }

    def get(self, resource, params=None, **kwargs):
        return self._get_response(resource, params, **kwargs)

    def post(self, resource, data=None, **kwargs):
        return self._get_response(resource, data, **kwargs)

    def patch(self, resource, data=None, **kwargs):
        return self._get_response(resource, data, **kwargs)

    def delete(self, resource, data=None, **kwargs):
        return self._get_response(resource, data, **kwargs)

    @res_error_handle
    def _get_response(self, resource, params, **kwargs):
        """
        server 에서 response 한 json text 를 dict 로 변환 후 반환 
        params 는 dict 객체에 파라미터 키,값을 넣어서 호출
        kwargs 에는 requests.requests 의 keyword arguments 그대로 전달

        @params resource : str
        @params params : dict
        @return : dict
        """
        url = self._build_url(resource)
        method = sys._getframe(2).f_code.co_name
        req_kwargs = self._get_method_kwargs(method, params, kwargs)
        req_kwargs = self._get_req_kwargs(req_kwargs)
        log.debug("url=%s, parmas=%s, method=%s, req_kwargs=%s", 
                   url, params, method, req_kwargs)
        self.res = requests.request(method, url, **req_kwargs)
        self._handle_response(self.res)
        return self.res.json()

    def _build_url(self, resource):
        if self.config["port"] == HTTPS_PORT:
            protocol = "https"
        else:
            protocol = "http"
        req_url = "{protocol}://{host}:{port}/{resource}".format(
            protocol=protocol, host=self.config["host"], port=self.config["port"],
            resource=resource)
        return req_url

    def _get_method_kwargs(self, method, params, kwargs):
        if params is None:
            return kwargs

        if method == "get":
            kwargs["params"] = params
        else:
            kwargs["data"] = params

        return kwargs

    def _get_req_kwargs(self, kwargs):
        for key, val in self.def_req_kwargs.items():
            if key in kwargs:
                continue
            else:
                kwargs[key] = val
        return kwargs

    def _handle_response(self, res):
        e = self.err_status_map.get(res.status_code, None)
        if e is not None:
            log.warning("ResponseError. status_code=%d, e=%s, url=%s", 
                        res.status_code, e, res.url)
            raise e

    @conf_error_handle
    def from_conf_file(self, name):
        cur_path = os.path.dirname(__file__)
        conf_path = os.path.join(cur_path, "conf.json")
        with open(conf_path) as f:
            json_str = f.read()
        cfg = json.loads(json_str)[name]
        self.config["host"] = cfg["host"]
        self.config["port"] = cfg["port"]
    