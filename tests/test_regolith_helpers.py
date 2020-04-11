import pytest
import os
from pathlib import Path, PurePath

from regolith_helpers.main import main

helper_map = [
    (["a_proprev",
      "A. Einstein", "nsf", "2020-04-08", "-q", "Tess Guebre",
      "-s", "downloaded", "-t", "A flat world theory"],
      "proposalReviews")]

@pytest.mark.parametrize("hm,outcollection", helper_map)
def test_regolith_helpers(hm, outcollection, make_db):
    repo = make_db
    tmp = Path(repo) / "local" / "fl"
    os.mkdir(tmp.parent)
    os.chdir(tmp.parent)
    main(argvs=hm)
    afile = Path(repo).joinpath("db", "{}.yml".format(outcollection))
    with open(afile, "r") as f:
        actual = f.read()
    efile = Path(PurePath(__file__).parent).joinpath("outputs", "{}.yml".format(
        outcollection))
    with open(efile, "r") as f:
        expected = f.read()
    assert actual == expected
