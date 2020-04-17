import datetime as dt
from ruamel import yaml
from pathlib import Path
import nameparser

from regolith.fsclient import dump_yaml
from regolith.dates import month_to_str_int

OUTCOLLECTION = 'proposalReviews'
ALLOWED_STATI = ["invited", "accepted", "declined", "downloaded", "inprogress",
                 "submitted", "cancelled"]


def subparser(subp):
    subpi = subp.add_parser("a_proprev", help="adds a new empty proposal review")
    subpi.add_argument("name", help="pi first name space last name in quotes",
                        default=None)
    subpi.add_argument("type", help="nsf or doe", default=None)
    subpi.add_argument("due_date", help="due date in form YYYY-MM-DD",
                        default=None)
    subpi.add_argument("-q", "--requester",
                        help="Name of the Program officer requesting"
                        )
    subpi.add_argument("-r", "--reviewer",
                        help="name of the reviewer.  Defaults to sbillinge")
    subpi.add_argument("-s", "--status",
                        help="status, from [invited, accepted, declined, downloaded,"
                             " inprogress, submitted, cancelled], default is accepted")
    subpi.add_argument("-t", "--title",
                        help="the title of the proposal")
    return subpi


def main(args):
    file = Path.cwd().joinpath('..', 'db', "{}.yml".format(OUTCOLLECTION))
    name = nameparser.HumanName(args.name)
    day = dt.datetime.today().day
    month = dt.datetime.today().month
    year = dt.datetime.today().year
    now = dt.datetime.now()
    key = "{}{}_{}_{}".format(
        str(year)[-2:], month_to_str_int(month), name.last.casefold(),
        name.first.casefold().strip("."))


    pdoc = {'adequacy_of_resources':['The resources available to the PI seem adequate'],
            'agency': args.type,
            'competency_of_team': [],
            'doe_appropriateness_of_approach': [],
            'doe_reasonableness_of_budget': [],
            'doe_relevance_to_program_mission': [],
            'does_how': [],
            'does_what': '',
            'due_date': args.due_date,
            'freewrite': [],
            'goals': [],
            'importance': [],
            'institutions': [],
            'month': 'tbd',
            'names': name.full_name,
            'nsf_broader_impacts': [],
            'nsf_create_original_transformative': [],
            'nsf_plan_good': [],
            'nsf_pot_to_advance_knowledge': [],
            'nsf_pot_to_benefit_society': [],
            'status': 'accepted',
            'summary': '',
            'year': 2020
            }

    if args.title:
        pdoc.update({'title': args.title})
    else:
        pdoc.update({'title': ''})
    if args.requester:
        pdoc.update({'requester': args.requester})
    else:
        pdoc.update({'requester': ''})
    if args.reviewer:
        pdoc.update({'reviewer': args.reviewer})
    else:
        pdoc.update({'reviewer': 'sbillinge'})
    if args.status:
        if args.status not in ALLOWED_STATI:
            raise ValueError("status should be one of {}".format(ALLOWED_STATI))
        else:
            pdoc.update({'status': args.status})
    else:
        pdoc.update({'status': 'accepted'})

    fullpdoc = {key: pdoc}
    sync_coll(file, fullpdoc)

    print("{} proposal has been added/updated in proposal reviews".format(args.name))
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
