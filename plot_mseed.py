from obspy import UTCDateTime
import os

class PlotMseed():
    def __init__(self, trace, filename, dayplot_directory):
        self._trace = trace
        self._filename = filename
        self._dayplot_directory = dayplot_directory

    def set_time(self):
        date = self._trace.stats.starttime.strftime('%Y-%m-%d')
        self._starttime=UTCDateTime(date+'T00:00:00.000000Z')
        self._endtime=UTCDateTime(date+'T23:59:59.990000Z')
        return self

    def plot(self):
        title = self._trace.stats.starttime.strftime('%Y-%m-%d')+' | '+self._trace.id+' | Sampling Rate: '+str(self._trace.stats.sampling_rate)+' | '+str(self._trace.stats.npts)+' samples'
        
        self.set_time()._trace.plot(type='dayplot', starttime=self._starttime, endtime=self._endtime, interval=60, one_tick_per_line=True, color=['k'], outfile=self._dayplot_directory+'.png', number_of_ticks=13, size=(1200,900), title=title, show=False)
        
        return self
