from airflow.hooks.base_hook import BaseHook


def get_db_url(conn_id) -> str:
    connection = BaseHook.get_connection(conn_id)
    return f'postgresql://{connection.login}:{connection.password}@{connection.host}:{connection.port}/{connection.schema}'