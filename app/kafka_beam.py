from __future__ import division, print_function

from abc import ABC

from apache_beam import PTransform, ParDo, DoFn, Create


class KafkaBeam(PTransform):

    def __init__(self, consumer_config, *args, **kwargs):
        super(KafkaBeam, self).__init__()
        self._config = consumer_config

    def expand(self, pcoll):
        print()
        return (
                pcoll
                | Create([self._config])
                | ParDo(_Consumer())
        )


class _Consumer(DoFn, ABC):

    def process(self, config):
        from kafka import KafkaConsumer
        kafka_client = KafkaConsumer("mamad23", bootstrap_servers="kafka-new.revolutlabs.com:9092",
                                     api_version=(0, 10, 1),
                                     group_id=config['group_id'])
        for msg in kafka_client:
            try:
                yield (msg.key, msg.value.decode())
            except Exception as e:
                print(e)
                continue
