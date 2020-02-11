# How to run the project 
```shell script
$ python setup.py sdist
```
```shell script
$ python -m main.py \
--runner DataflowRunner \
--project revolut-ds \
--temp_location gs://revolut-ds/tmp/ \
--subnetwork https://www.googleapis.com/compute/v1/projects/revolut-ds/regions/europe-west1/subnetworks/default \
--staging_location=gs://revolut-ds/tmp/ \
--extra_package=dist/app-1.0.0.tar.gz \
--setup_file=./setup.py
```