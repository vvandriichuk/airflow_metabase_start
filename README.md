# airflow_metabase_start

На сервере у вас может возникать ошибка PermissionError: [Errno 13] Permission denied: '/opt/airflow/logs/scheduler/'. Исправить нужно так: зайти в директорию airflow и выполить команду:

~~~
chmod -R 777 logs/
~~~

Далее необходимо перейти в директорию airflow и выполнить там команду

~~~
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
~~~

Подробнее можете прочитать здесь: https://airflow.apache.org/docs/apache-airflow/2.1.3/docker-compose.yaml

