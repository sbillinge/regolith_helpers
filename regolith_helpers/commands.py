"""Implementation of commands for command line."""
import os
from pprint import pprint
import re
import json
import sys

from regolith.tools import string_types
from regolith.builder import builder, BUILDERS
from regolith.emailer import emailer as email
from regolith.deploy import deploy as dploy

RE_AND = re.compile("\s+and\s+")
RE_SPACE = re.compile("\s+")

INGEST_COLL_LU = {".bib": "citations"}

def new(rc):

def add_cmd(rc):
    """Adds documents to a collection in a database."""
    db = rc.client[rc.db]
    coll = db[rc.coll]
    docs = [
        json.loads(doc) if isinstance(doc, string_types) else doc
        for doc in rc.documents
    ]
    rc.client.insert_many(rc.db, rc.coll, docs)


def build_db_check(rc):
    """Checks which DBs a builder needs"""
    dbs = set()
    for t in rc.build_targets:
        bldr = BUILDERS[t]
        needed_dbs = getattr(bldr, 'needed_dbs', None)
        # If the requested builder doesn't state DB deps then it requires
        # all dbs!
        if not needed_dbs:
            return None
        dbs.update(needed_dbs)
    return dbs


def build(rc):
    """Builds all of the build targets"""
    for t in rc.build_targets:
        bldr = builder(t, rc)
        bldr.build()


def deploy(rc):
    """Deploys all of the deployment targets."""
    if not hasattr(rc, "deploy") or len(rc.deploy) == 0:
        raise RuntimeError("run control has no deployment targets!")
    for target in rc.deploy:
        dploy(rc, **target)


def classlist(rc):
    """Sets values for the class list."""
    from regolith.classlist import register

    register(rc)


def json_to_yaml(rc):
    """Converts JSON to YAML"""
    from regolith import fsclient

    for inp in rc.files:
        base, ext = os.path.splitext(inp)
        out = base + ".yaml"
        fsclient.json_to_yaml(inp, out)


def yaml_to_json(rc):
    """Converts YAML to JSON"""
    from regolith import fsclient

    for inp in rc.files:
        base, ext = os.path.splitext(inp)
        out = base + ".json"
        fsclient.yaml_to_json(inp, out)


def validate(rc):
    """Validate the combined database against the schemas"""
    from regolith.schemas import validate

    print("=" * 10 + "\nVALIDATING\n")
    any_errors = False
    if getattr(rc, "collection"):
        db = {rc.collection: rc.client.chained_db[rc.collection]}
    else:
        db = rc.client.chained_db
    for name, collection in db.items():
        errored_print = False
        for doc_id, doc in collection.items():
            v = validate(name, doc, rc.schemas)
            if v[0] is False:
                if errored_print is False:
                    errored_print = True
                    any_errors = True
                    print("Errors found in {}".format(name))
                    print("=" * len("Errors found in {}".format(name)))
                print("ERROR in {}:".format(doc_id))
                pprint(v[1])
                for vv in v[1]:
                    pprint(doc.get(vv))
                print("-" * 15)
                print("\n")
    if not any_errors:
        print("\nNO ERRORS IN DBS\n" + "=" * 15)
    else:
        sys.exit("Validation failed on some records")
