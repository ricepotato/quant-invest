#-*- coding: utf-8 -*-

import logging

log = logging.getLogger("qi.data.calc")

class ERData:
    """ earning ratio Data """
    def __init__(self):
        self.er_dao = None
        self.comp_dao = None
        self.calc = None

    def add(self, data: dict) -> int:
        """ 
        er data 입력
        code, st_date, hold, period, group=None
        """
        group = data.get("group", 0)
        return self.er_dao.insert(data["code"], data["st_date"], data["hold"], 
                                  data["period"], group)

    def get(self, group: int=None) -> list:
        """ group 으로 등록된 er data 를 가져온다. """
        if group is None:
            group = 0

        res = self.er_dao.select(group=group)
        if not res:
            return []

        def _rs_func(item):
            res = self.calc.get_list(item["code"], item["st_date"], 
                                     item["hold"], item["period"])
            res["period"] = item["period"]
            res["hold"] = item["hold"]
            comp_res = self.comp_dao.select(code=item["code"])
            if comp_res:
                res["comp_name"] = comp_res[0].name
            return res
                
        return list(map(lambda item: _rs_func(item), res))
