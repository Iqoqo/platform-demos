from builtins import range
from iqoqo import iqoqo_job
from prime_finder_task import find_primes

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator

args = {
    'owner': 'iqoqo_airflow_user',
    'start_date': airflow.utils.dates.days_ago(1),
}

dag = DAG(
    dag_id='iqoqo_python_operator',
    default_args=args,
    schedule_interval=None,
)

step = 5
ranges = [(n, min(n + step, 100)) for n in range(0, 100, step)]

for i in range(step):
    also_run_this = BashOperator(
    task_id='analyze_primes_' + str(i),
    bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    # python_callable=find_primes,
    op_kwargs={'start_range': ranges[i][0], 'end_range': ranges[i][1]},
    dag=dag,
)
