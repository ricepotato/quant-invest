#-*- coding: utf-8 -*-
import logging

class LogCfg(object):
    def __init__(self):
        self.HDLR_NAME_STREAM = 'stream'
        self.log = logging.getLogger('qi')
        self.log.setLevel(logging.INFO)
        self.default_fmt = logging.Formatter("[%(name)s|%(filename)s:%(lineno)d"
                                             "|P:%(process)d|T:%(thread)d"
                                             "|%(levelname)s] %(message)s")
        self.simple_fmt = logging.Formatter("[%(asctime)s|%(name)s"
                                            "|%(filename)s|%(lineno)d"
                                            "|%(levelname)s] %(message)s")
        self._add_handlers()
        

    def set_level(level):
        self.log.setLevel(level)

    def get_handler(self, name):
        for hdlr in self.log.handlers:
            hdlr_name = hdlr.get_name()
            if name == hdlr_name:
                return hdlr

        return None

    def add_stream_handler(self):
        hdlr = self.get_handler(self.HDLR_NAME_STREAM)
        if hdlr is None:
            self.log.addHandler(self._stream_handler())

    def _add_handlers(self):
        self.add_stream_handler()

    def _stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.set_name(self.HDLR_NAME_STREAM)
        stream_handler.setFormatter(self.simple_fmt)
        return stream_handler

qi_logger = LogCfg().log
