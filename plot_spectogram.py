from obspy import UTCDateTime

class PlotSpectogram():
    def __init__(self, trace, filename, spectogram_directory):
        self._trace = trace
        self._filename = filename
        self._spectogram_directory = spectogram_directory

    def set_time(self):
        date = self._trace.stats.starttime.strftime('%Y-%m-%d')
        self._starttime=UTCDateTime(date+'T00:00:00.000000Z')
        self._endtime=UTCDateTime(date+'T23:59:59.990000Z')
        return self

    def plot(self):
        title = self._trace.stats.starttime.strftime('%Y-%m-%d')+' | '+self._trace.id+' | '+str(self._trace.stats.sampling_rate)+'Hz | '+str(self._trace.stats.npts)+' samples'

        '''
        Dokumentasi
        https://docs.obspy.org/_modules/obspy/imaging/spectrogram.html
        '''
        self.set_time()._trace.spectrogram(wlen=600, per_lap=0.5, outfile=self._spectogram_directory+'.png', title=title, show=False)

        return self

