from ftplib import FTP
from datetime import datetime, timedelta
import ntpath
import requests
from io import IOBase
from copy import copy
import operator
from .sv import SemSV, YumaSV
from .utils import AlmanacFormats
from io import BytesIO

class Ephemeris:
    __FTP_URL = 'cddis.nasa.gov'
    __FTP_BASE_PATH = 'gnss/data/'
    __FTP_FILE_FORMAT_DAILY = 'daily/%Y/{:03d}/%yn/brdc{:03d}0.%yn.Z'
    __FTP_FILE_FORMAT_HOURLY = 'hourly/%Y/{:03d}/hour{:03d}0.%yn.Z'
    __RETR_CMD = 'RETR '

    @staticmethod
    def get_daily_raw(writable, date = datetime.now()) -> str:
        """fills writable and returns name of the ephemeris for the input date by day"""
        return Ephemeris.__get_ephemeris(writable, date, Ephemeris.__FTP_BASE_PATH + Ephemeris.__FTP_FILE_FORMAT_DAILY)

    @staticmethod
    def get_hourly_raw(writable, date = datetime.now()) -> str:
        """fills writable and returns name of the ephemeris for the input date by hour"""
        return Ephemeris.__get_ephemeris(writable, date, Ephemeris.__FTP_BASE_PATH + Ephemeris.__FTP_FILE_FORMAT_HOURLY)

    @staticmethod
    def __get_path(date, str) -> (str, str):
        """Generates the ftp path for the ephemeris"""
        day_of_year = (date - datetime(date.year, 1, 1)).days + 1
        ftp_path = date.strftime(str).format(day_of_year, day_of_year)
        file_name = ntpath.basename(ftp_path)
        return (ftp_path, file_name)

    @staticmethod
    def __get_ephemeris(buffer, date, format) -> str:
        """Connects to the FTP to retrieve the ephemeris with the given format"""
        # Open FTP connection
        ftp = FTP(Ephemeris.__FTP_URL)
        ftp.login()
        # Generate Path to file
        (ftp_path, file_name) = Ephemeris.__get_path(date, format)
        # Download File
        ftp.retrbinary(Ephemeris.__RETR_CMD + ftp_path, buffer.write) 
        ftp.quit()
        return file_name

class Almanac:
    __TEXT_FORMAT = 'UTF-8'
    __SPLIT_FORMAT = ' '
    __ALM_URL = 'https://navcen.uscg.gov/?pageName=currentAlmanac&format='
    __ALMANAC_TYPES = ['yuma', 'yuma-txt', 'sem', 'sem-txt']
    __ALMANAC_EXT = ['.alm', '.txt', '.al3', '.txt']
    __FILE_NAME_FORMAT = 'almanac_%Y_%m_%d_%H_%M_%S'

    def __init__(self):
        self.space_vehicles = {}
        self.type = None

    def parse(self, text_buf: IOBase, type: int) -> bool:
        """Parses an almanac file with the given type"""
        self.space_vehicles.clear()
        self.type = type

        if type == AlmanacFormats.YUMA_TEXT:
            sv = YumaSV()
            while sv.parse_text(text_buf):
                if sv.prn != 0:
                    self.space_vehicles[sv.prn] = copy(sv)
        elif type == AlmanacFormats.SEM_TEXT:
            sv = SemSV()
            sv_count = int(text_buf.readline().decode(Almanac.__TEXT_FORMAT).split(Almanac.__SPLIT_FORMAT)[0])
            line_split = text_buf.readline().decode(Almanac.__TEXT_FORMAT).strip().split(Almanac.__SPLIT_FORMAT)
            week = int(line_split[0])
            time = int(line_split[1])
            for _ in range(0, sv_count):
                text_buf.readline()#throwaway blank line
                if sv.parse_text(text_buf):
                    sv.week = week
                    sv.time_of_applicability_s = time
                    if sv.prn != 0:
                        self.space_vehicles[sv.prn] = copy(sv)
        else:
            return False
        return True

    @staticmethod
    def get_current(type: AlmanacFormats) -> 'Almanac':
        """Retrieves and parses the current almanac"""
        format = None
        if type == AlmanacFormats.YUMA or type == AlmanacFormats.YUMA_TEXT:
            format = AlmanacFormats.YUMA_TEXT
        elif type == AlmanacFormats.SEM or type == AlmanacFormats.SEM_TEXT:
            format = AlmanacFormats.SEM_TEXT
        else:
            return None

        bytes = BytesIO()
        alm = Almanac()
        Almanac.get_current_raw(bytes, format)
        bytes.seek(0)
        alm.parse(bytes, format)
        return alm

    # return the almanac for the current day
    @staticmethod
    def get_current_raw(buffer, type = AlmanacFormats.YUMA) -> str:
        """Retrieves the current almanac and writes it to the buffer"""
        r = requests.get(Almanac.__ALM_URL + Almanac.__ALMANAC_TYPES[int(type)], allow_redirects=True)
        buffer.write(r.content)
        return datetime.now().strftime(Almanac.__FILE_NAME_FORMAT) + Almanac.__ALMANAC_EXT[int(type)]
