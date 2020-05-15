from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators import KubernetesOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.pod import Port
from airflow.operators.dummy_operator import DummyOperator

default_args={
   'owner':'airflow',
   'start_date': datetime.utcnow()
}

dag = DAG('a_kubernetes_sample', default_args=default_args, schedule_interval=timedelta(minutes=10))

start = DummyOperator(task_id='run_this_first', dag=dag)
passing = KubernetesPodOperator(namespace='airflow',
                          image="k8soperator/test",
                          cmds=["sh","test.sh"],
                          labels={"foo": "bar"},
                          name="passing-test",
                          task_id="passing-task",
                          get_logs=True,
                          dag=dag
                          )
