
#-*- coding: utf-8 -*-
# Python 3.6

# *****************************************************************************
#
#   brief   exceptions
#  
#   file    exc.py
#   date    2019-08-01
#   author  sukjun.sagong@ahnlab.com
#
#   par     Copyright
#   Copyright (C) 2019 AhnLab, Inc. All rights reserved.
#   Any part of this source code can not be copied with any method without
#   prior written permission from the author or authorized person.
#
# *****************************************************************************

class ApiError(Exception):
    pass

class ResponseError(ApiError):
    """ server 결과값, 처리 에러 json 아님 등 """
    pass

class NoContent(ResponseError):
    pass

class ServerError(ResponseError):
    pass

class NotFound(ResponseError):
    pass

class BadRequest(ResponseError):
    pass

class ConnectionError(ApiError):
    """ server connection error, timeout error 등 """
    pass

class ConfigError(ApiError):
    """ config 파일에 객체에 이름이 없거나 conf 파일 없음 등 """
    pass

class ExecutionError(ApiError):
    """ API App 실행 시 에러 """
    pass