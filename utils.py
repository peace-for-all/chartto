import datetime
import time

def date2d3(date):
    """Converts date string into nvd3 format for timeseries
       ref: http://acaird.github.io/2015/08/12/nvd3-time-series-plots
    """
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()) * 1000