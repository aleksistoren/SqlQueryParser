from collections import defaultdict

import pytest
import sqlglot

from main import parse_statement

@pytest.mark.parametrize("sql_query, expected_result", [
    (
        "SELECT a.* FROM table_a AS a",
        defaultdict(set, {"table_a": {'*'}})
    ),
    (
        "SELECT a.id, b.name FROM table_a AS a JOIN table_b AS b ON a.id = b.a_id",
        defaultdict(set, {"table_a": {'id'}, "table_b": {'name', 'a_id'}})
    ),
    (
        "SELECT COUNT(*), b.name FROM table_b AS b",
        defaultdict(set, {"table_b": {'*'}})
    ),
    (
        "SELECT a.id, a.name FROM table_a AS a WHERE a.id > 10",
        defaultdict(set, {"table_a": {'id', 'name'}})
    ),
])
def test_extract_tables_and_columns(sql_query, expected_result):
    assert parse_statement(sql_query) == expected_result

# Дополнительные тесты могут быть добавлены аналогичным образом
