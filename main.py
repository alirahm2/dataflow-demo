import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from app import kafka_beam as kf
from app import rest_beam as re
import signal
import time
import subprocess
import logging as log


class MyTest:
    def __init__(self) -> None:
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        self.pipe_config = None
        self.running_flag = True

    def run_pipeline(self):
        try:
            pipeline = beam.Pipeline(
                options=PipelineOptions(streaming=True, save_main_session=True)
            )
            process_line = pipeline | "Reading records from kafka" >> kf.KafkaBeam(
                {"group_id": "andi"}
            )
            process_line | "Send to rest endpoint" >> re.RestBeam(
                {"url": "http://localhost:2020"}
            )

            self.pipe_config = pipeline.run()
            log.info("::: JOB DEPLOYED :::")

            while self.running_flag:
                log.info("::: JOB RUNNING :::")
                time.sleep(1)

        except Exception as e:
            log.info("ERROR")

    def stop(self, signum, frame):
        self.running_flag = False
        status_checking_flag = True
        job_id = self.pipe_config.job_id()
        subprocess.call(
            f'gcloud dataflow jobs cancel {job_id} --region="europe-west1"', shell=True
        )
        while status_checking_flag:
            result = subprocess.Popen(
                f'gcloud dataflow jobs list  --region="europe-west1" --filter="{job_id}"|cut -d" " -f 10',
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            for line in result.stdout.readlines():
                line_as_txt = line.decode("utf-8").upper()
                log.info(line_as_txt)
                if "CANCELLED" in line_as_txt:
                    status_checking_flag = False
            time.sleep(1)

        log.info("::: JOB TERMINATED :::")


log.basicConfig(level=log.INFO)
logger = log.getLogger(__name__)

andi = MyTest()
andi.run_pipeline()
