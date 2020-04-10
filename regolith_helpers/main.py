"""The main CLI for regolith-helpers"""
from argparse import ArgumentParser
from regolith_helpers import add_proposal_review

def create_parser():
    p = ArgumentParser()
    subp = p.add_subparsers(title="cmd", dest="cmd")

    add_proposal_review.subparser(subp)
    return p

def main(argvs=None):
    parser = create_parser()
    ns = parser.parse_args(argvs)
    if ns.cmd == 'a_proprev':
       add_proposal_review.main(ns)


if __name__ == "__main__":
    main()
