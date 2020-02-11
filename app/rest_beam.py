from abc import ABC

from apache_beam import PTransform, ParDo, DoFn
import logging as log
import requests


class RestBeam(PTransform):
    def __init__(self, endpoint_address):
        super(RestBeam, self).__init__()
        self._endpoint_addr = endpoint_address

    def expand(self, pcoll):
        return pcoll | ParDo(_RestEndpointMessage(self._endpoint_addr))


class _RestEndpointMessage(DoFn, ABC):
    def __init__(self, endpoint, *args, **kwargs):
        super(_RestEndpointMessage, self).__init__(*args, **kwargs)
        self.config = endpoint

    def process(self, element):
        try:
            log.info(element[1])
            requests.post(self.config["url"], element[1])
        except Exception as e:
            log.info("error in rest endpoint")
