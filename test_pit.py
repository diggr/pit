#!/usr/bin/env python3
"""
This file contains the software tests.
"""

from click.testing import CliRunner
from pit.tool import cli


def setup_module():
    global runner
    runner = CliRunner()


def test_empty_argument():
    result = runner.invoke(cli)
    assert result.exit_code == 2


def test_path_as_argument():
    result = runner.invoke(cli, ["."])
    assert result.exit_code == 1
