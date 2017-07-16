# coding: utf-8
import pytest

from trackr import Trackr
from trackr.carriers.base import Package, TrackingInfo
from trackr.exceptions import PackageNotFound

from .. import trackr_vcr


@trackr_vcr.use_cassette
def test_ect_tracking_ok():
    p = Trackr.track('ect', 'PN871429404BR')

    assert isinstance(p, Package)
    assert p.object_id == 'PN871429404BR'

    for t in p.tracking_info:
        assert isinstance(t, TrackingInfo)


@trackr_vcr.use_cassette
def test_ect_tracking_not_found():
    with pytest.raises(PackageNotFound) as exc_info:
        Trackr.track('ect', 'SX123456789BR')
        assert exc_info.value.object_id == 'SX123456789BR'


@trackr_vcr.use_cassette
def test_ect_tracking_bulk_ok():
    object_ids = [
        'PO454515464BR',
        'OA473577210BR',
        'OA468082105BR',
    ]

    items = Trackr.track(
        'ect',
        object_ids,
    )

    for i, item in enumerate(items):
        assert item.object_id == object_ids[i]
