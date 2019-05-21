
import logging

class LogCfg(object):
    def __init__(self):
        self.HDLR_NAME_STREAM = 'stream'
        self.log = logging.getLogger('qi')
        self._add_handlers()

    def _add_handlers(self):
        pass

    def _stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.set_name(self.HDLR_NAME_STREAM)
        return stream_handler

qi_logger = LogCfg().log