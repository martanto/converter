from obspy import read, Trace, Stream
import datetime
import os
import numpy
from settings import settings
from scan import Scan
from new_stream import NewStream
from plot_mseed import PlotMseed

"""
SDS Directory https://www.seiscomp3.org/doc/applications/slarchive/SDS.html
Channel naming https://ds.iris.edu/ds/nodes/dmc/data/formats/seed-channel-naming/
"""
class ConvertToMseed():
    
    def __init__(self):
        self._directory = settings['directory']
        self._output_directory = settings['output_directory']
        self._dayplot_directory = settings['dayplot_directory']
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

    def sds(self):
        """
        <SDSdir>/Year/NET/STA/CHAN.TYPE/NET.STA.LOC.CHAN.TYPE.YEAR.DAY
        """
        s = self._dict_structure
        path = os.path.join(self._output_directory,'SDS',s['year'],s['network'],s['station'],s['channel']+'.'+s['type'])
        self.filename = '.'.join([s['network'],s['station'],s['location'],s['channel'],s['type'],s['year'],s['julian_day']])
        self.check_directory(path)
        return os.path.join(path,self.filename)

    def get_folder(self, trace):
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
            return self.sds()
        elif settings['data_structure'] == 'plain':
            return self.plain()    
        return self.idds()

    def check_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        return self

    def file_not_exists(self, file):
        return not os.path.exists(file)

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
                for trace in new_stream:
                    if self.file_not_exists(self.get_folder(trace)):
                        print(trace)
                        self.save(trace, self.get_folder(trace))

    def save(self, trace, path):
        try:
            print('==== Saving Seismogram ')
            trace.write(path+'.mseed', format='MSEED')
            self.plot(trace, self.filename, self._dayplot_directory)
        except:
            trace.data = trace.data.clip(-2e30, 2e30)
            print('==== Saving Seismogram ')
            trace.write(path+'.mseed', format='MSEED')
            self.plot(trace, self.filename, self._dayplot_directory)
        return self

    def plot(self, trace, filename, dayplot_directory):
        PlotMseed(trace, filename, dayplot_directory).plot()

    def convert_and_plot(self):
        pass