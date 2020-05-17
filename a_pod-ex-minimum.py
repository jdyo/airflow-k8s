import datetime
from airflow import models
from airflow.contrib.operators import kubernetes_pod_operator
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)
dag=models.DAG(
            dag_id='a_pod-ex-minimum',
            schedule_interval=datetime.timedelta(days=1),
            start_date=YESTERDAY) 

volume_mount = VolumeMount(name='mykube-volume',
                           mount_path='/usr/local/airflow/etc/',
                           sub_path=None,
                           read_only=True)

volume_config= {
    'hostPath':
      {
        'path': '/usr/local/airflow/etc'
      }
    }
volume = Volume(name='mykube-volume', configs=volume_config)

        
kubernetes_min_pod = kubernetes_pod_operator.KubernetesPodOperator(
        # The ID specified for the task.
        task_id='pod-ex-minimum',
        # Name of task you want to run, used to generate Pod ID.
        dag=dag,
        name='pod-ex-minimum',
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=['echo'],
        config_file="/usr/local/airflow/etc/config",
        volumes=[volume],
        volume_mounts=[volume_mount],
        # The namespace to run within Kubernetes, default namespace is
        # `default`. There is the potential for the resource starvation of
        # Airflow workers and scheduler within the Cloud Composer environment,
        # the recommended solution is to increase the amount of nodes in order
        # to satisfy the computing requirements. Alternatively, launching pods
        # into a custom namespace will stop fighting over resources.
        namespace='airflow',
        # Docker image specified. Defaults to hub.docker.com, but any fully
        # qualified URLs will point to a custom repository. Supports private
        # gcr.io images if the Composer Environment is under the same
        # project-id as the gcr.io images and the service account that Composer
        # uses has permission to access the Google Container Registry
        # (the default service account has permission)
        image='ubuntu:16.04')
