from apache_beam import PTransform, ParDo, DoFn
import logging as log

class RestBeam(PTransform):

    def __init__(self, endpoint_address):
        super(RestBeam, self).__init__()
        self._endpoint_addr = endpoint_address

    def expand(self, pcoll):
        return (
                pcoll
                | ParDo(_RestEndpointMessage(self._endpoint_addr))
        )


class _RestEndpointMessage(DoFn):

    def __init__(self, endpoint, *args, **kwargs):
        super(_RestEndpointMessage, self).__init__(*args, **kwargs)
        self.attributes = endpoint

    def process(self, element):
        try:
            log.warning("sent")
        except Exception as e:
            raise
