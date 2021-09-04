# airflow_metabase_start

На сервере у вас может возникать ошибка PermissionError: [Errno 13] Permission denied: '/opt/airflow/logs/scheduler/'. Исправить нужно так: зайти в директорию airflow и выполить команду: chmod -R 777 logs/
