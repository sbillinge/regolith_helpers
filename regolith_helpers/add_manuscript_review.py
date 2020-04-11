import datetime as dt
from ruamel import yaml
from pathlib import Path
import nameparser

from regolith.fsclient import dump_yaml
from regolith.dates import month_to_str_int

OUTCOLLECTION = 'refereeReports'
ALLOWED_STATI = ["invited", "accepted", "declined", "downloaded", "inprogress",
                 "submitted"]


def subparser(subp):
    subpi = subp.add_parser("a_manrev", help="adds a new empty manuscript review")
    subpi.add_argument("last", help="first author last name",
                        default=None)
    subpi.add_argument("journal", help="the journal asking for the review", default=None)
    subpi.add_argument("due_date", help="due date in form YYYY-MM-DD",
                        default=None)
    subpi.add_argument("-r", "--reviewer",
                        help="name of the reviewer.  Defaults to sbillinge")
    subpi.add_argument("-s", "--status",
                        help="status, from [invited, accepted, declined, downloaded,"
                             "inprogress, submitted], default is accepted")
    subpi.add_argument("-t", "--title",
                        help="the title of the proposal")
    return subpi


def main(args):
    file = Path.cwd().joinpath('..', 'db', "{}.yml".format(OUTCOLLECTION))
    sync_coll(file, {})

    month = dt.datetime.today().month
    year = dt.datetime.today().year
    now = dt.datetime.now()
    key = "{}{}_{}".format(
        str(year)[-2:], month_to_str_int(month), args.last.casefold())


    pdoc = {'claimed_found_what': [],
            'claimed_why_important': [],
            'did_how': [],
            'did_what': [],
            'due_date': args.due_date,
            'editor_eyes_only': '',
            'first_author_last_name': args.last,
            'final_assessment': [],
            'freewrite': '',
            'journal': args.journal,
            'month': 'tbd',
            'recommendation': '',
            'status': 'accepted',
            'validity_assessment': [],
            'year': 2020
            }
    if args.reviewer:
        pdoc.update({'reviewer': args.reviewer})
    else:
        pdoc.update({'reviewer': 'sbillinge'})
    if args.status:
        if args.status not in ALLOWED_STATI:
            raise ValueError("status should be one of {}".format(ALLOWED_STATI))
        else:
            pdoc.update({'status': args.status})
    if args.title:
        pdoc.update({'title': args.title})
    else:
        pdoc.update({'title': ''})
    fullpdoc = {key: pdoc}
    sync_coll(file, fullpdoc)

    print("{} proposal has been added/updated in proposal reviews".format(args.last))
    return fullpdoc


def sync_coll(collfile, dict):
    with open(collfile, "r", encoding='utf8') as i:
        current = yaml.safe_load(i)
    current.update(dict)
    for k, v in current.items():
        v.update({"_id": k})
    dump_yaml(collfile, current)


if __name__ == '__main__':
    main()

