

class _SqlGenerator:
    def __init__(self):
        pass

    # Vérifié

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
    
    @staticmethod
    def _generate_cols_names(cols_names: list[str]):
        return ", ".join(cols_names)
    
    # A vérifier
    def generate_select(self, table_name: str, columns_names: list[str] = ["*"], **kwargs):
        columns = self._generate_cols_names(cols_names=columns_names)
        query = f"SELECT {columns} FROM `{table_name}`"
        if "where" in kwargs:
            query += f" WHERE {kwargs['where']}"
        if "order_by" in kwargs:
            query += f" ORDER BY {kwargs['order_by']}"
        if "limit" in kwargs:
            query += f" LIMIT {kwargs['limit']}"
        return query
    
    def generate_join(self,
                      left_table_name: str,
                      left_ref_col: str,
                      right_table_name: str,
                      right_ref_col: str,
                      join_type: str = "LEFT"):
        return f"""
            {join_type} JOIN `{right_table_name}`
            ON `{left_table_name}`.`{left_ref_col}` = `{right_table_name}`.`{right_ref_col}`
        """
    
    def generate_select_join(self,
                             left_table_name: str,
                             left_ref_col: str,
                             right_table_name: str,
                             right_ref_col: str,
                             columns_names: tuple[list[str]] | None = None,  # (left, right) or None for all columns
                             **kwargs):
        
        if columns_names is not None:
            left_cols, right_cols = columns_names
            left_columns_names = [f"`{left_table_name}`.{col}" for col in left_cols]
            right_columns_names = [f"`{right_table_name}`.{col}" for col in right_cols]
            columns_names = left_columns_names + right_columns_names
        
        query = self.generate_select(table_name=left_table_name,
                                     columns_names=columns_names,
                                     **kwargs)
        query += self.generate_join(left_table_name=left_table_name,
                                    left_ref_col=left_ref_col,
                                    right_table_name=right_table_name,
                                    right_ref_col=right_ref_col)
        return query
    