from io import IOBase
from .utils import AlmanacFormats

class SemSV:
    def __init__(self):
        self.week = 0
        self.time_of_applicability_s = 0
        self.prn = 0
        self.svn = 0
        self.average_ura = 0
        self.eccentricity = 0
        self.inclination_offset = 0
        self.rate_of_right_ascen = 0
        self.sqrt_semi_major_axis = 0
        self.geo_long_of_orbital_plane = 0
        self.arg_of_perigree = 0
        self.mean_anomaly = 0
        self.zeroth_order_clock_correction = 0
        self.first_order_clock_correction = 0
        self.health = 0
        self.configuration = 0

    def parse_text(self, text_buffer: IOBase):
        """Parses a single sv from a Sem text formatted Almanac file"""
        self.prn = int(text_buffer.readline().split()[0])
        self.svn = int(text_buffer.readline().split()[0])
        self.average_ura = float(text_buffer.readline().split()[0])
        line = text_buffer.readline().split()
        self.eccentricity = float(line[0])
        self.inclination_offset = float(line[1])
        self.rate_of_right_ascen = float(line[2])
        line = text_buffer.readline().split()
        self.sqrt_semi_major_axis = float(line[0])
        self.geo_long_of_orbital_plane = float(line[1])
        self.arg_of_perigree = float(line[2])
        line = text_buffer.readline().split()
        self.mean_anomaly = float(line[0])
        self.zeroth_order_clock_correction = float(line[1])
        self.first_order_clock_correction = float(line[2])
        self.health = int(text_buffer.readline().split()[0])
        self.configuration = int(text_buffer.readline().split()[0])
        return True

class YumaSV:
        _SPLIT_CHAR = ':'
        _TEXT_FORMAT = 'UTF-8'
        _PRN_STR = 'PRN-'
        _PRN_STR_LEN = len(_PRN_STR)
        _PRN_NUM_LEN = 2

        def __init__(self):
            self.prn = 0
            self.id = 0
            self.health = 0
            self.eccentricity = 0
            self.time_of_applicability_s = 0
            self.orbital_inclication_rad = 0
            self.rate_of_right_ascen_rps = 0
            self.sqrt_a_m_to_1o2 = 0
            self.right_ascen_at_week_rad = 0
            self.arg_of_perig_rad = 0
            self.mean_anom_rad = 0
            self.af0_s = 0
            self.af1_sos = 0
            self.week = 0        
        
        def parse_text(self, text_buffer: IOBase) -> bool:
            """Parses a single sv from a Yuma text formatted Almanac file"""
            prn_line = text_buffer.readline().decode(YumaSV._TEXT_FORMAT).strip()
            if not prn_line: return False
            prn_start = prn_line.find(YumaSV._PRN_STR) + YumaSV._PRN_STR_LEN
            self.prn = int(prn_line[prn_start: prn_start + YumaSV._PRN_NUM_LEN])
            self.id = YumaSV.__parse_txt_line(int, text_buffer)
            self.health = YumaSV.__parse_txt_line(int, text_buffer)
            self.eccentricity = YumaSV.__parse_txt_line(float, text_buffer)
            self.time_of_applicability_s = YumaSV.__parse_txt_line(float, text_buffer)
            self.orbital_inclication_rad = YumaSV.__parse_txt_line(float, text_buffer)
            self.rate_of_right_ascen_rps = YumaSV.__parse_txt_line(float, text_buffer)
            self.sqrt_a_m_to_1o2 = YumaSV.__parse_txt_line(float, text_buffer)
            self.right_ascen_at_week_rad = YumaSV.__parse_txt_line(float, text_buffer)
            self.arg_of_perig_rad = YumaSV.__parse_txt_line(float, text_buffer)
            self.mean_anom_rad = YumaSV.__parse_txt_line(float, text_buffer)
            self.af0_s = YumaSV.__parse_txt_line(float, text_buffer)
            self.af1_sos = YumaSV.__parse_txt_line(float, text_buffer)
            self.week = YumaSV.__parse_txt_line(float, text_buffer)
            line = text_buffer.readline()
            stripped = line.strip()
            if not stripped:
                text_buffer.seek(len(line), 1)
            return True

        @staticmethod 
        def __parse_txt_line(func, text_buffer):
            """Reads a single line, splits based on split char"""
            line = text_buffer.readline().decode(YumaSV._TEXT_FORMAT)
            split = line.split(YumaSV._SPLIT_CHAR)
            return func(split[1].strip())