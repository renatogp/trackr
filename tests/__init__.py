# coding: utf-8
import vcr

trackr_vcr = vcr.VCR(
    cassette_library_dir='tests/recorded',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)
