from collections import defaultdict
from typing import Optional

import sqlglot

QUERY = "SELECT a.*, b.column1, b.column2 FROM table_a AS a JOIN table_b AS b ON a.id = b.a_id"


def extract_tables_and_columns(query: str) -> defaultdict:
    columns = defaultdict(list)
    parsed_expr = sqlglot.parse_one(query)
    return columns


def main():
    extract_tables_and_columns()


if __name__ == '__main__':
    main()
