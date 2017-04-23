#!/usr/bin/env python
# coding: utf-8

from click.testing import CliRunner

from trackr import cli

from . import trackr_vcr


@trackr_vcr.use_cassette
def test_command_line_interface_package_found():
    runner = CliRunner()

    help_result = runner.invoke(
        cli.main, ['--carrier', 'ect', '--object-id', 'PN871429404BR'])
    assert help_result.exit_code == 0
    assert 'Package found!' in help_result.output


@trackr_vcr.use_cassette
def test_command_line_interface_package_not_found():
    runner = CliRunner()

    help_result = runner.invoke(
        cli.main, ['--carrier', 'ect', '--object-id', 'SX123456789BR'])
    assert help_result.exit_code == 0
    assert 'Package with object ID SX123456789BR (ect) not found' in help_result.output
