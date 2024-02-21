import uuid
from collections import defaultdict
from typing import List

import sqlglot
from sqlglot.optimizer import build_scope, traverse_scope
from sqlglot import exp, Schema, MappingSchema
from sqlglot.optimizer.qualify_columns import qualify_columns


class SqlQueryParser:
    @classmethod
    def parse_statement(cls, sql_query: str) -> defaultdict[List[str]]:
        all_table_name = f'ALL{uuid.uuid4().hex}'
        updated_query = sql_query.replace('.*', f'.{all_table_name}')
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

    @classmethod
    def extract_fields_from_formula(cls, formula):
        table = f'TABLE{uuid.uuid4().hex}'
        res = cls.parse_statement(f"SELECT {formula} FROM {table}")

        return res[table]