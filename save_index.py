from models.index_file import IndexFile

def sds_index(filename,trace,date):
    print('* SDS Indexing '+str(trace)+' ====')
    index = IndexFile()
    index.filename = filename
    index.scnl = get_scnl(trace)
    index.sampling_rate = get_sampling_rate(trace)
    index.date = date
    index.max_amplitude = float(abs(trace.max()))
    index.availability = get_availability(trace)
    index.save()

def get_scnl(trace):
    scnl = trace.stats.station+'_'+trace.stats.channel+'_'+trace.stats.network+'_'+trace.stats.location
    return scnl

def get_sampling_rate(trace):
    return float(round(trace.stats.sampling_rate, 2))

def get_availability(trace):
    availability = float(round(trace.stats.npts/8640000*100,2))
    return availability

if __name__ == '__main__':
    sds_index()