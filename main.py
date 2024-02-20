import uuid
from collections import defaultdict


import sqlglot
from sqlglot.optimizer import build_scope, traverse_scope
from sqlglot import exp, Schema, MappingSchema
from sqlglot.optimizer.qualify_columns import qualify_columns

# QUERY = "SELECT a.*, b.column1, b.column2 FROM table_a AS a JOIN table_b AS b ON a.id = b.a_id"

QUERY = f'''SELECT 
    a.ALL{uuid.uuid4().hex}, 
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

q = 'toDecimal(col44, 20) / nullif(toDecimal(col10, 20), 0)'


def parse_statement(sql_query):
    all_table_name = f'ALL{uuid.uuid4().hex}'
    updated_query = sql_query.replace('*', all_table_name)
    ast = sqlglot.parse_one(updated_query, dialect='clickhouse')
    ast = qualify_columns(ast, schema=None)

    physical_columns = defaultdict(set)

    for scope in traverse_scope(ast):
        for c in scope.columns:
            if isinstance(scope.sources.get(c.table), exp.Table):
                physical_columns[scope.sources.get(c.table).name].add(c.name)

    for table in list(physical_columns.keys()):
        if all_table_name in physical_columns[table]:
            physical_columns[table] = {'*'}

    return physical_columns


def extract_fields_from_formula(formula):
    table = f'TABLE{uuid.uuid4().hex}'
    res = parse_statement(f"SELECT {formula} FROM {table}")

    return res[table]


def main():
    res = extract_fields_from_formula(q)
    print(res)

    res = parse_statement(QUERY)
    print(res)


if __name__ == '__main__':
    main()
