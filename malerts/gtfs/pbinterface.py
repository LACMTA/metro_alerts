# -*- coding: utf-8 -*-

class PBtransfer:
    def fromProtoBuf(self, pb2, attrs = None):
        if not attrs:
            attrs = self.pb_rows
        for attr in attrs:
            setattr(self, attr, getattr(pb2, attrs[attr]))

    def toProtoBuf(self, pb2, attrs = None):
        if not attrs:
            attrs = self.pb_rows
        for attr in attrs.keys():
            setattr(pb2, attrs[attr], getattr(self, attr))
        return pb2


