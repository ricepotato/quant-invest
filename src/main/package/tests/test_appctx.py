#-*- coding: utf-8 -*-
import os
import logging
import unittest

from qi.appctx import AppContext
from qi.appctx.exc import *
from ctx_test.some import SomeObj

log = logging.getLogger("qi.tests.appctx")

ctx = {
    "SomeObj1":{
        "class":"ctx_test.some.SomeObj"
    },
    "SomeObjWithArgs":{
        "class":"ctx_test.some.SomeObjWithArg",
        "init_args":[
            {"value":3}, {"value":4}
        ]
    },
    "SomeObjWithAK":{
        "class":"ctx_test.some.SomeObjWithArgsKwargs",
        "init_args":[
            {"value":5}
        ],
        "init_kwargs":{
            "name":{"value":10},
            "obj":{"bean":"SomeObj1"}
        },
        "properties":{
            "address":{"value":"addr"},
            "some_obj":{"bean":"SomeObj1"}
        }
    },
    "SomeObjInvalidPath":{
        "class":"ctx_test.invalid.path"
    }
}

class TestAppContext(unittest.TestCase):
    def setUp(self):
        self.ctx = AppContext(ctx)
    
    def tearDown(self):
        pass

    def test_get_bean_invalid_name(self):
        with self.assertRaises(InvalidBeanName) as context:
            obj = self.ctx.get_bean("invalidname")

    def test_get_bean(self):
        obj = self.ctx.get_bean("SomeObj1")
        self.assertTrue(isinstance(obj, SomeObj))

    def test_get_bean_with_args(self):
        obj = self.ctx.get_bean("SomeObjWithArgs")
        self.assertEqual(obj.arg1, 3)
        self.assertEqual(obj.arg2, 4)

    def test_get_bean_ak(self):
        obj = self.ctx.get_bean("SomeObjWithAK")
        self.assertEqual(obj.arg1, 5)
        self.assertEqual(obj.kwargs["name"], 10)
        self.assertTrue(isinstance(obj.kwargs["obj"], SomeObj))
        self.assertEqual(obj.address, "addr")
        self.assertTrue(isinstance(obj.some_obj, SomeObj))

    def test_get_bean_invalid_path(self):
        with self.assertRaises(InvalidModulePath) as context:
            obj = self.ctx.get_bean("SomeObjInvalidPath")

if __name__ == "__main__":
    unittest.main()