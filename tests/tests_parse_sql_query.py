from collections import defaultdict

import pytest

from sql_query_parser import SqlQueryParser


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
    (
            '''SELECT 
                a.*, 
                b.column1, 
                b.column2, 
                c.aggregated_column
            FROM 
                table_a AS a 
            JOIN 
                table_b AS b ON a.id = b.a_id
            JOIN (
                SELECT 
                    table_c.a_id, 
                    SUM(table_c.some_column) AS aggregated_column
                FROM 
                    table_c
                GROUP BY 
                    table_c.a_id
            ) AS c ON a.id = c.a_id
            WHERE 
                b.column2 > (SELECT AVG(d.column3) FROM table_d AS d WHERE d.b_id = b.id)
            ''',
    defaultdict(set,{'table_a': {'*'},
                     'table_b': {'column2', 'id', 'a_id', 'column1'},
                     'table_c': {'some_column', 'a_id'},
                     'table_d': {'b_id', 'column3'}})
    )
])
def test_extract_tables_and_columns(sql_query, expected_result):
    assert SqlQueryParser.parse_statement(sql_query) == expected_result

# Дополнительные тесты могут быть добавлены аналогичным образом
