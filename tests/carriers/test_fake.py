# coding: utf-8
import pytest

from trackr import Trackr
from trackr.carriers.base import Package, TrackingInfo


def test_fake_tracking_single_object():
    p = Trackr.track('fake', 'SX123456789BR')

    assert isinstance(p, Package)
    assert p.object_id == 'SX123456789BR'

    for t in p.tracking_info:
        assert isinstance(t, TrackingInfo)


def test_fake_tracking_bulk():
    with pytest.raises(NotImplementedError):
        Trackr.track('fake', ['1', '2'])
