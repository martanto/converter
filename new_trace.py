import numpy

class NewTrace():

    def __init__(self, trace, network='VG', channel='EHZ', location='00', skip_check=True):
        self._trace = trace
        self._trace.stats['network'] = network
        self._trace.stats['channel'] = trace.stats.channel if len(trace.stats.channel) > 2 else trace.stats.channel+trace.stats.location
        self._trace.stats['location'] = location
        self._skip_check = skip_check

    def set_network(self, station):
        self._trace.stats['station'] = station
        return self

    def set_channel(self, channel):
        self._trace.stats['channel'] = channel
        return self
    
    def set_location(self, location):
        self._trace.stats['location'] = location
        return self

    def check_data_dtype(self):
        """
        trace.data.dtype
        """
        if self._trace.data.dtype == numpy.int32:
            return self
        else:  
            self._trace.data.dtype = numpy.int32
            return self

    def check_sampling_rate(self):
        if self._trace.stats.sampling_rate == 100.0:
            return self
        else:
            self._trace.resample(100.0)
            return self

    def get(self):
        if self._skip_check:
            return self._trace
        else:
            self.check_sampling_rate().check_data_dtype()
            return self._trace