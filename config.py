# -*- coding: utf-8 -*-
"""
配置

@author: hch
@date  : 2021/12/8
"""
from configparser import ConfigParser

import yaml


class Conf(dict):
    app_conf = None
    ymls = set()
    confs = set()

    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    @classmethod
    def from_file_yml(cls, file):
        with open(file) as f:
            conf = yaml.safe_load(f)
            if cls.app_conf:
                cls.app_conf.update_attr(conf)
            else:
                cls.app_conf = cls.dict_to_obj(conf)
            cls.ymls.add(file)

    @classmethod
    def from_file_conf(cls, file):
        cp = ConfigParser()
        cp.read(file, encoding='utf-8')
        conf = {s: dict(cp.items(s)) for s in cp.sections()}
        if cls.app_conf:
            cls.app_conf.update_attr(conf)
        else:
            cls.app_conf = cls.dict_to_obj(conf)
        cls.confs.add(file)

    @classmethod
    def refresh(cls):
        if cls.app_conf is None:
            return
        for f in cls.ymls:
            cls.from_file_yml(f)
        for f in cls.confs:
            cls.from_file_conf(f)

    def update_attr(self, attr):
        for k, v in attr.items():
            self[k] = Conf.dict_to_obj(v)

    @staticmethod
    def dict_to_obj(dict_obj):
        if not isinstance(dict_obj, dict):
            return dict_obj
        d = Conf()
        for k, v in dict_obj.items():
            d[k] = Conf.dict_to_obj(v)
        return d


Conf.from_file_yml('conf/app.yml')
Conf.from_file_conf('conf/credentials.conf')
Conf.from_file_conf('conf/city.conf')
APP_CONF = Conf.app_conf

if __name__ == '__main__':
    Conf.from_file_yml('conf/app.yml')
    Conf.from_file_conf('conf/city.conf')
    print(Conf.app_conf.wx.user)
    import time

    time.sleep(8)
    Conf.refresh()
    print(Conf.app_conf.wx.user)
