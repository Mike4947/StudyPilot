import argparse
from .agenda import Agenda, Entry


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="bringstudy",
        description="BringStudy - agenda for students aged 14-18",
    )
    sub = parser.add_subparsers(dest="cmd")

    add_p = sub.add_parser("add", help="Add a new agenda entry")
    add_p.add_argument("title", help="Short title for the entry")
    add_p.add_argument("date", help="Date of the entry (YYYY-MM-DD)")
    add_p.add_argument(
        "-c", "--category", default="note", help="Category such as exam or schedule"
    )
    add_p.add_argument("-d", "--description", default="", help="Optional description")

    sub.add_parser("list", help="List all entries")

    args = parser.parse_args()
    agenda = Agenda()

    if args.cmd == "add":
        entry = Entry(
            title=args.title,
            date=args.date,
            category=args.category,
            description=args.description,
        )
        agenda.add_entry(entry)
        print("Entry added")
    else:
        for entry in agenda.list_entries():
            print(f"{entry.date} [{entry.category}] {entry.title} - {entry.description}")


if __name__ == "__main__":
    main()
