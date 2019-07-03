from builtins import range
from datetime import timedelta

import airflow
from boto3 import client
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

IQOQO_LOGIN_USER = 'zohar.sacks@iqoqo.co';
IQOQO_LOGIN_PASSWORD = '12345678';

def list_remote_files():
    bucket_name = "iqoqo.airflow.demo"
    prefix      = "Food-5K"

    s3_conn   = client('s3', region_name='us-east-2')  
    s3_result =  s3_conn.list_objects_v2(Bucket=bucket_name, Prefix=prefix,Delimiter = "/Food-5K")

    if 'Contents' not in s3_result:
        print("ERROR" + s3_result)
        return []

    file_list = []
    for key in s3_result['Contents']:
        file_list.append(key['Key'])
    print(f"List count = {len(file_list)}")

    while s3_result['IsTruncated']:
        continuation_key = s3_result['NextContinuationToken']
        s3_result = s3_conn.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter="/Food-5K", ContinuationToken=continuation_key)

        for key in s3_result['Contents']:
            file_list.append(key['Key'])

        print(f"List count = {len(file_list)}")
    return file_list


args = {
    'owner': 'iqoqo_sample',
    'start_date': airflow.utils.dates.days_ago(1),
}

dag = DAG(
    dag_id='iqoqo_bash_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60),
)

run_this = BashOperator(
    task_id='analyze_existing_images',
    bash_command='echo 1',
    dag=dag,
)

iqoqo_login = BashOperator(
    task_id='iqoqo_login',
    bash_command="iqoqo login -u " + IQOQO_LOGIN_USER + " -p " + IQOQO_LOGIN_PASSWORD,
    dag=dag,
)

analyze_unknown_images = BashOperator(
    task_id='analyze_unknown_images',
    bash_command="iqoqo add -n 'analyze_unknown_images' -s predict.py -r -w -t",
    dag=dag,
)

run_this >> iqoqo_login

for i in range(5):
    task_id='extract_features_from_images_' + str(i)
    task = BashOperator(
        task_id=task_id,    
        bash_command='iqoqo add -n '+str(task_id)+' -s extract_features.py -r -w -t imgs_str_'+str(i),
        dag=dag,
    )
    task >> run_this

build_model = BashOperator(
    task_id='build_model',
    bash_command='iqoqo add -n '+str(task_id)+' -s train.py -r -w -t',
    dag=dag,
)

build_model >> iqoqo_login
analyze_unknown_images >> build_model





if __name__ == "__main__":
    remotefileList = list_remote_files()
    dag.cli()
