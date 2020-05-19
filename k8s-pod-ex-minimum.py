import datetime
from airflow import models
from airflow.contrib.operators import kubernetes_pod_operator
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)
dag=models.DAG(
            dag_id='k8s-pod-ex-minimum',
            schedule_interval=datetime.timedelta(days=1),
            start_date=YESTERDAY) 
        
kubernetes_min_pod = kubernetes_pod_operator.KubernetesPodOperator(
        # The ID specified for the task.
        task_id='pod-ex-minimum',
        # Name of task you want to run, used to generate Pod ID.
        dag=dag,
        name='pod-ex-minimum',
        cmds=['echo'],
        config_file="/usr/local/airflow/etc/kube.config",
        namespace='airflow',
        image='ubuntu:16.04')
