

class _SqlGenerator:
    def __init__(self):
        pass

    def generate_select(self, table_name: str, columns_names: list[str] | None = None, **kwargs):
        columns = "*"
        if columns_names is not None:
            columns = ", ".join(columns_names)
        query = f"SELECT {columns} FROM `{table_name}`"
        if "where" in kwargs:
            query += f" WHERE {kwargs['where']}"
        if "order_by" in kwargs:
            query += f" ORDER BY {kwargs['order_by']}"
        if "limit" in kwargs:
            query += f" LIMIT {kwargs['limit']}"
        return query
    
    def _generate_where_clause(self,
                               where_column_name: str,
                               where_value: str | None = None, # None for null values
                               where_operator: str = "="): 
        if where_value is None:
            return f"WHERE `{where_column_name}` IS NULL"
        return f"WHERE `{where_column_name}` {where_operator} '{where_value}'"


    def generate_update(self,
                        table_name: str,
                        column_name: str,
                        value: str,
                        where_column_name: str | None = None,  # None for all rows
                        where_value: str | None = None,  # None for null values
                        where_operator: str = "="):  #
        query = f"""
            UPDATE `{table_name}`
            SET `{column_name}` = {value}
            """
        
        if where_column_name is not None:
            query += self._generate_where_clause(where_column_name=where_column_name,
                                                 where_value=where_value,
                                                 where_operator=where_operator)
            
        return query
    