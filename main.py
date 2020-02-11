import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from app import kafka_beam as kf
import signal
import time
import subprocess

config = {"group_id": "andi"}


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
            process_line = pipeline | "Reading month records" >> kf.KafkaBeam(config)
            # process_line | 'Send to rest' >> re.RestBeam("10:10:10")

            self.pipe_config = pipeline.run()
            print("::: JOB DEPLOYED :::")

            while self.running_flag:
                time.sleep(1)
                print("::: JOB RUNNING :::")

        except Exception as e:
            print("ERROR")

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
                print(line_as_txt)
                if "CANCELLED" in line_as_txt:
                    status_checking_flag = False
            time.sleep(1)
        print("::: JOB TERMINATED :::")


andi = MyTest()
andi.run_pipeline()
