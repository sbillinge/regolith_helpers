import pytest
import os
from pathlib import Path, PurePath

from local.new_proposal_review import main

OUTCOLLECTION = "proposalReviews"

def test_main(make_db):
    repo = make_db
    print(repo)
    tmp = Path(repo) / "local" / "fl"
    os.mkdir(tmp.parent)
    os.chdir(tmp.parent)
    main(argvs=["A. Einstein", "nsf", "2020-04-08",
                "-q", "Tess Guebre",
                "-s", "downloaded",
                "-t", "A flat world theory"])
    afile = Path(repo).joinpath("db", "{}.yml".format(OUTCOLLECTION))
    with open(afile, "r") as f:
        actual = f.read()
    efile = Path(PurePath(__file__).parent).joinpath("outputs", "{}.yml".format(OUTCOLLECTION))
    with open(efile, "r") as f:
        expected = f.read()
    assert actual == expected
