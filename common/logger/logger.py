
import logging

class LogCfg(object):
    def __init__(self):
        self.HDLR_NAME_STREAM = 'stream'
        self.log = logging.getLogger('qi')
        self.default_fmt = logging.Formatter("[%(name)s|%(filename)s:%(lineno)d"
                                             "|P:%(process)d|T:%(thread)d"
                                             "|%(levelname)s] %(message)s")
        self.simple_fmt = logging.Formatter("[%(asctime)s|%(name)s"
                                            "|%(filename)s|%(lineno)d"
                                            "|%(levelname)s] %(message)s")
        self._add_handlers()

    def get_handler(self, name):
        for hdlr in self.log.handlers:
            hdlr_name = hdlr.get_name()
            if name == hdlr_name:
                return hdlr

        return None

    def add_stream_handler(self):
        pass

    def _add_handlers(self):
        pass

    def _stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.set_name(self.HDLR_NAME_STREAM)
        return stream_handler

qi_logger = LogCfg().log