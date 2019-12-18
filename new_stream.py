from obspy import Stream, read
from new_trace import NewTrace
import os

class NewStream():
    def __init__(self, stream_file, sampling_rate=100.0):
        self._stream = stream_file
        self._sampling_rate = sampling_rate
   
    def get(self):
        list_traces = []
        try:
            self._stream = read(pathname_or_url=self._stream)
            for trace in self._stream:
                if trace.stats.sampling_rate < 50.0:
                    self._stream.remove(trace)
                else:
                    new_trace = NewTrace(trace).get()
                    list_traces.append(new_trace)

            return Stream(list_traces)
        except:
            os.remove(self._stream)
            pass
