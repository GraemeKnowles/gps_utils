from gps_utils import files
from io import BytesIO

def test_alm():
    with BytesIO() as buf:
        files.get_current_almanac(buf)
    assert True

def test_deph():
    with BytesIO() as buf:
        files.get_daily_ephemeris(buf)
    assert True

def test_heph():
    with BytesIO() as buf:
        files.get_hourly_ephemeris(buf)
    assert True