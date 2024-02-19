import pytest
import sqlglot

from main import extract_tables_and_columns

@pytest.mark.parametrize("sql_query, expected_result", [
    (
            "SELECT a.* FROM table_a AS a",
            {"table_a": set(['*'])}
    ),
    (
            "SELECT a.id, b.name FROM table_a AS a JOIN table_b AS b ON a.id = b.a_id",
            {"table_a": set(['id']), "table_b": set(['name'])}
    ),
    (
            "SELECT COUNT(*), b.name FROM table_b AS b",
            {"table_b": set(['name', '*'])}
    ),
    (
            "SELECT a.id, a.name FROM table_a AS a WHERE a.id > 10",
            {"table_a": set(['id', 'name'])}
    ),
])
def test_extract_tables_and_columns(sql_query, expected_result):
    assert extract_tables_and_columns(sql_query) == expected_result

# Дополнительные тесты могут быть добавлены аналогичным образом
