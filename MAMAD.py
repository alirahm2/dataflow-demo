import subprocess
import time

job_id = "2020-02-11_05_12_35-4164646621548658729"
out = subprocess.Popen(f'gcloud dataflow jobs list  --region="europe-west1" --filter="{job_id}"|cut -d" " -f 10', shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while True:
    out = subprocess.Popen(f'gcloud dataflow jobs list  --region="europe-west1" --filter="{job_id}"|cut -d" " -f 10',
                           shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in out.stdout.readlines():
        print(line.decode("utf-8") )
        print("Cancelled" in line.decode("utf-8"))
        print("------")
    time.sleep(1)
