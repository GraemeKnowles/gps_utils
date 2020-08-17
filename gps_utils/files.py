from ftplib import FTP
from datetime import datetime, timedelta
import ntpath
import requests

__FTP_URL = 'cddis.nasa.gov'
__FTP_BASE_PATH = 'gnss/data/'
__FTP_FILE_FORMAT_DAILY = 'daily/%Y/{:03d}/%yn/brdc{:03d}0.%yn.Z'
__FTP_FILE_FORMAT_HOURLY = 'hourly/%Y/{:03d}/hour{:03d}0.%yn.Z'
__RETR_CMD = 'RETR '

__ALM_URL = 'https://navcen.uscg.gov/?pageName=currentAlmanac&format='
__ALMANAC_TYPES = ['yuma', 'yuma-txt', 'sem', 'sem-txt']

class Almanac_Types:
    Yuma = 0
    Yuma_Text = 1
    Sem = 2
    Sem_Text = 3

# filles writable and returns file name of the ephemeris for the input date by day
def get_daily_ephemeris(writable, date = datetime.now()):
    return __get_ephemeris(writable, date,__FTP_BASE_PATH + __FTP_FILE_FORMAT_DAILY)

# fills writable and returns file name of the ephemeris for the input date by hour
def get_hourly_ephemeris(writable, date = datetime.now()):
    return __get_ephemeris(writable, date, __FTP_BASE_PATH + __FTP_FILE_FORMAT_HOURLY)

# return the almanac for the current day
def get_current_almanac(buffer, type = Almanac_Types.Yuma):
    r = requests.get(__ALM_URL + __ALMANAC_TYPES[type], allow_redirects=True)
    buffer.write(r.content)
    return buffer

# connects to ftp and retrieves 
def __get_ephemeris(buffer, date, format):
    # Open FTP connection
    ftp = FTP(__FTP_URL)
    ftp.login()
    # Generate Path to file
    (ftp_path, file_name) = __get_path(date, format)
    # Download File
    ftp.retrbinary(__RETR_CMD + ftp_path, buffer.write) 
    ftp.quit()
    return file_name

# generate path to file for input date
def __get_path(date, str):
    day_of_year = (date - datetime(date.year, 1, 1)).days + 1
    ftp_path = date.strftime(str).format(day_of_year, day_of_year)
    file_name = ntpath.basename(ftp_path)
    return (ftp_path, file_name)