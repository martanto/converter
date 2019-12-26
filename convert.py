from obspy import read, Trace, Stream
import datetime
import os
from multiprocessing import Pool
from settings import settings
from scan import Scan
from new_stream import NewStream
from plot_mseed import PlotMseed
from plot_spectogram import PlotSpectogram
from save_index import sds_index

"""
SDS Directory https://www.seiscomp3.org/doc/applications/slarchive/SDS.html
Channel naming https://ds.iris.edu/ds/nodes/dmc/data/formats/seed-channel-naming/
"""
class ConvertToMseed():
    
    def __init__(self):
        self._directory = settings['directory']
        self._output_directory = settings['output_directory']
        self._dayplot_directory = settings['dayplot_directory']
        self._spectogram_directory = settings['spectogram_directory']
        self._start_date = settings['start_date']
        self._end_date = settings['end_date']

    def set_directory(self, directory):
        self._directory = directory
        return self

    def set_output_directory(self, output_directory):
        self._output_directory = output_directory
        return self

    def set_dayplot_directory(self, dayplot_directory):
        self._dayplot_directory = dayplot_directory
        return self

    def set_start_date(self, start_date):
        self._start_date = start_date
        return self

    def set_end_date(self, end_date):
        self._end_date = end_date
        return self

    def date_format(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def date_range(self):
        start = self.date_format(self._start_date)
        end = self.date_format(self._end_date)
        for n in range(int((end-start).days)+1):
            yield start+datetime.timedelta(n)

    def sds(self, output_directory):
        """
        <SDSdir>/Year/NET/STA/CHAN.TYPE/NET.STA.LOC.CHAN.TYPE.YEAR.DAY
        """
        s = self._dict_structure
        path = os.path.join(output_directory,'SDS',s['year'],s['network'],s['station'],s['channel']+'.'+s['type'])
        self.filename = '.'.join([s['network'],s['station'],s['location'],s['channel'],s['type'],s['year'],s['julian_day']])
        self.check_directory(path)
        return os.path.join(path,self.filename)

    def get_folder(self, trace, output_directory):
        self._dict_structure = {
            'year' : trace.stats.starttime.strftime('%Y'),
            'julian_day' : trace.stats.starttime.strftime('%j'),
            'station' : trace.stats.station,
            'channel' : trace.stats.channel,
            'type' : 'D',
            'network': trace.stats.network,
            'location': '00'
        }
        
        if settings['data_structure'] == 'sds':
            return self.sds(output_directory)
        elif settings['data_structure'] == 'plain':
            return self.plain(output_directory)    
        return self.idds()

    def check_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        return self

    def file_not_exists(self, file):
        return not os.path.exists(file+'.mseed')

    def _save(self, trace, path):
        trace.write(path+'.mseed', format='MSEED')

    def save(self, trace, path):
        try:
            self._save(trace, path)
        except:
            trace.data = trace.data.clip(-2e30, 2e30)
            self._save(trace, path)
        return self

    def plot(self, trace, filename, dayplot_directory):
        PlotMseed(trace, filename, dayplot_directory).plot()

    def spectogram(self, trace, filename, spectogram_directory):
        PlotSpectogram(trace, filename, spectogram_directory).plot()

    def convert(self):
        print('=== Converting Only ===')
        for date in self.date_range():
            print('>>> Start : '+date.strftime('%Y-%m-%d'))
            stream_files = Scan().set_filter(date.strftime('%Y-%m-%d')).get_files()
            if len(stream_files) > 0:
                new_stream = Stream()
                for stream_file in stream_files:
                    new_stream += NewStream(stream_file).get()
                new_stream = new_stream.merge(fill_value=0)
                for index, trace in enumerate(new_stream, start=1):
                    if self.file_not_exists(self.get_folder(trace, self._output_directory)):
                        print(str(index)+'. '+str(trace)+' | Max : '+str(abs(trace.max())))
                        self.save(trace, self.get_folder(trace, self._output_directory))

    def convert_and_plot(self, use_cpu=2):
        print('=== Converting and Plot Daily Seismogram ===')
        print('=== Jumlah CPU yang digunakan : ',use_cpu,' ===')
        pool = Pool(use_cpu)
        pool.map(self._multi_convert_and_plot, self.date_range())
        return self

    def _multi_convert_and_plot(self, date):
        string_date = date.strftime('%Y-%m-%d')
        print('>>> Start : '+string_date)
        stream_files = Scan().set_filter(string_date).get_files()
        if len(stream_files) > 0:
            new_stream = Stream()
            for stream_file in stream_files:
                new_stream += NewStream(stream_file).get()
            new_stream = new_stream.merge(fill_value=0)
            print('==== Saving Seismogram '+string_date+' ====')
            for index, trace in enumerate(new_stream, start=1):
                if self.file_not_exists(self.get_folder(trace, self._output_directory)):
                    print(str(index)+'. '+str(trace)+' | Max : '+str(abs(trace.max())))
                    self.save(trace, self.get_folder(trace, self._output_directory))
                    self.plot(trace, self.filename, self.get_folder(trace, self._dayplot_directory))
                    # self.spectogram(trace, self.filename, self.get_folder(trace, self._spectogram_directory))
                sds_index(filename=self.filename,trace=trace,date=string_date)
