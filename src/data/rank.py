#-*- coding: utf-8 -*-

import os
import sys
import copy
import logging

cur_path = os.path.dirname(__file__)
base_path = os.path.abspath(os.path.join(cur_path, ".."))

sys.path.append(base_path)

log = logging.getLogger('qi.data.rank')

DESC = 1
ASC = -1

def cmp_func(x, y):
    if x is None and y is None:
        return 0
    elif x is None:
        return 1
    elif y is None:
        return -1
    else:
        if x > y:
            return 1
        elif x < y:
            return -1
        else:
            return 0

def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

class Rank(object):
    def __init__(self, data):
        self.data = data
        self.sort_columns = []
    
    def add_rank_column(self, name, order):
        self.sort_columns.append({"name":name, "order":order})

    def _add_total_rank_prop(self, data):
        copied_data = copy.deepcopy(data)
        for item in copied_data:
            total = 0
            for column in self.sort_columns:
                total += item["{}_rank".format(column["name"])]

            item["total_rank"] = total
        return copied_data

    def _add_rank_prop(self, sorted_data, prep_name):
        rank = 1
        idx = 0
        copied_data = copy.deepcopy(sorted_data)
        try:
            while True:
                if idx > 0 and copied_data[idx-1][prep_name] == \
                    copied_data[idx][prep_name]:
                    copied_data[idx]["{}_rank".format(prep_name)] = \
                        copied_data[idx-1]["{}_rank".format(prep_name)]
                else:
                    copied_data[idx]["{}_rank".format(prep_name)] = rank
                idx += 1
                rank += 1
                if idx == len(copied_data):
                    break
        except (KeyError, IndexError) as e:
            log.warning("_add_rank_prop error. %s", e)
            return sorted_data
        return copied_data

    def get_rank(self):
        sorted_list = []        
        for sort_item in self.sort_columns:
            if sort_item["order"] == DESC:
                reverse = True
            else:
                reverse = False
            
            def cmp(src, dest):
                return cmp_func(src[sort_item["name"]], 
                                dest[sort_item["name"]])    
            
            sorted_data = sorted(self.data, key=cmp_to_key(cmp), reverse=reverse)
            self.data = self._add_rank_prop(sorted_data, sort_item["name"])

        res_data = self._add_total_rank_prop(self.data)
        key_func = lambda item:item["total_rank"]
        self.data = sorted(res_data, key=key_func)
        return self.data
