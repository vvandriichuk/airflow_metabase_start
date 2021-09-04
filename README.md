# airflow_metabase_start

На сервере у вас может возникать ошибка PermissionError: [Errno 13] Permission denied: '/opt/airflow/logs/scheduler/'. Исправить нужно так: зайти в директорию airflow и выполить команду:

~~~
chmod -R 777 logs/
~~~

Далее необходимо перейти в директорию airflow и выполнить там команду

~~~
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
~~~

и потом дописать то, что будет в .env в docker-compose.yml

что-то типа такого

~~~
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor
    AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0
    AIRFLOW__CORE__FERNET_KEY: ''
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
    AIRFLOW__CORE__LOAD_EXAMPLES: 'true'
    AIRFLOW__API__AUTH_BACKEND: 'airflow.api.auth.backend.basic_auth'
    _PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}
    AIRFLOW_UID: 0
    AIRFLOW_GID: 0
~~~

Подробнее можете прочитать здесь: https://airflow.apache.org/docs/apache-airflow/2.1.3/docker-compose.yaml и здесь https://www.bigdataschool.ru/blog/apache-airflow-installation.html

После выполнения всех действий выше запустите команду в корне Вашего проекта:

~~~
bash run_docker.sh
~~~

