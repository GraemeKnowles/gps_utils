from gps_utils import files
from io import BytesIO
from gps_utils.utils import AlmanacFormats

__MAX_SPACE_VEHICLES = 31

def check_alm(almanac:files.Almanac):
    correct_vehicles = len(almanac.space_vehicles) == __MAX_SPACE_VEHICLES
    correct_prn = almanac.space_vehicles[1].prn == 1
    assert correct_vehicles and correct_prn

def test_alm_yuma_text():
    check_alm(files.Almanac.get_current(AlmanacFormats.YUMA_TEXT))

def test_alm_sem_text():
    check_alm(files.Almanac.get_current(AlmanacFormats.SEM_TEXT))

def test_daily_eph_raw():
    with BytesIO() as buf:
        files.Ephemeris.get_daily_raw(buf)
        with open('daily_eph.txt', 'wb') as f:
            f.write(buf.getbuffer())
    assert True

def test_hourly_eph_raw():
    with BytesIO() as buf:
        files.Ephemeris.get_hourly_raw(buf)
        with open('hourly_eph.txt', 'wb') as f:
            f.write(buf.getbuffer())
    assert True