# coding: utf-8

from trackr import Trackr
from trackr.carriers.base import Package, TrackingInfo


def test_fake_tracking():
    p = Trackr.track('fake', 'SX123456789BR')

    assert isinstance(p, Package)
    assert p.object_id == 'SX123456789BR'

    for t in p.tracking_info:
        assert isinstance(t, TrackingInfo)
