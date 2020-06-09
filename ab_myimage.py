import datetime
from airflow import models
from airflow.contrib.operators import kubernetes_pod_operator

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)
dag=models.DAG(
            dag_id='ab_pod-ex-minimum',
            schedule_interval=datetime.timedelta(days=1),
            start_date=YESTERDAY) 
        
kubernetes_min_pod = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='pod-ex-minimum-u',
        dag=dag,
        name='pod-ex-minimum-u',
        cmds=['/bin/bash','/test.sh'],
        #config_file="/var/airflow/secrets/kubeconfig/kube.config",
        namespace='airflow',
        image='ubuntu:jdyo')
