import json
import pytest

from pathlib import Path
from ..utils import provit_uri, load_jsonld, walk_up


def test_provit_uri():
    assert (
        provit_uri("test123abc") == "http://vocab.ub.uni-leipzig.de/provit/test123abc"
    )


def test_load_jsonld(tmp_path):
    test_file = tmp_path / "test_123"
    assert load_jsonld(test_file) == (None, None)
    test_file.touch()
    assert load_jsonld(test_file) == (None, None)
    with open(test_file, "w") as tfile:
        json.dump([], tfile)
    assert load_jsonld(test_file) == (None, None)
    with open(test_file, "w") as tfile:
        json.dump([1, 2, 3], tfile)
    with pytest.raises(IOError):
        load_jsonld(test_file)


def test_walk_up(tmp_path):
    str_path = str(tmp_path.resolve()).split("/")
    for p, path in enumerate(walk_up(tmp_path)):
        if p != len(str_path) - 1:
            assert path == "/".join(str_path[: len(str_path) - p])
        else:
            assert path == "/"
