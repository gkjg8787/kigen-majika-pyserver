from enum import Enum
import sys
import argparse

from model.database import db_util


class DBCommandName(Enum):
    CREATE = "create"
    DROP = "drop"
    RECREATE = "recreate"


def parse_paramter(argv):
    parser = argparse.ArgumentParser(description="table create and drop")
    parser.add_argument("name", type=str, choices=[v.value for v in DBCommandName])

    args = parser.parse_args(argv[1:])
    return args


def main(argv):
    param = parse_paramter(argv)
    if param.name == DBCommandName.RECREATE.value:
        db_util.remove_db()
        db_util.create_db()
        return
    if param.name == DBCommandName.CREATE.value:
        db_util.create_db()
        return
    if param.name == DBCommandName.DROP.value:
        db_util.remove_db()
        return
    return


if __name__ == "__main__":
    main(sys.argv)
