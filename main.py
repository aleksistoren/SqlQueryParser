from collections import defaultdict
from typing import Optional

import sqlglot
from sqlglot.optimizer import build_scope, traverse_scope
from sqlglot import exp
from sqlglot.optimizer.qualify_columns import qualify_columns


#QUERY = "SELECT a.*, b.column1, b.column2 FROM table_a AS a JOIN table_b AS b ON a.id = b.a_id"

QUERY = '''SELECT 
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
'''


def parse_statement(sql_query):
    ast = sqlglot.parse_one(sql_query)
    ast = qualify_columns(ast, schema=None)

    physical_columns = defaultdict(set)

    for scope in traverse_scope(ast):
        for c in scope.columns:
            if isinstance(scope.sources.get(c.table), exp.Table):
                physical_columns[scope.sources.get(c.table).name].add(c.name)

    return physical_columns

def main():
    res = parse_statement(QUERY)
    print(res)

if __name__ == '__main__':
    main()
