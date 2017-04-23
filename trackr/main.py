# -*- coding: utf-8 -*-
from .carriers import registry


class Trackr(object):

    @classmethod
    def track(cls, carrier_id, object_id, **carrier_kwargs):
        return registry[carrier_id](**carrier_kwargs).track(object_id)
