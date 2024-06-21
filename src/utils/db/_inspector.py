from sqlalchemy import inspect


class _DbInspector:
    # TODO : create an inspector class from scratch ?
    def __init__(self, engine):
        self._inspector = inspect(engine)

    def list_columns(self, table_name: str):
        return self._inspector.get_columns(table_name)

    def list_table_names(self):
        return self._inspector.get_table_names()

    def list_columns_names(self, table_name: str):
        return [col["name"] for col in self._inspector.get_columns(table_name)]
    
    def detect_column_sql_type(self, table_name: str, column_name: str):
        column_info = self._inspector.get_columns(table_name)
        column_type = None

        for col in column_info:
            if col["name"] == column_name:
                column_type = col["type"]
                break
        if column_type is None:
            raise ValueError(f"Column '{column_name}' not found in table '{table_name}'")
        return column_type
    