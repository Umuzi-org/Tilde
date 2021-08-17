import datetime
import pytz

# import re


# def get_timezone_name(iso_tz_info: str):
#     """ eg if you have a time string that looks like this "Tue Oct 18 12:25:50 2016 +0200"

#     then the iso_tz_info is the "+0200" part.

#     get_timezone_name("+0200") would then return
#     """
#     assert re.match("^[+-]\d{4}$", iso_tz_info), f"Maldormed timezone string {iso_tz_info}"

#     hour = int(iso_tz_info[1:3])
#     minute = int(iso_tz_info[3:])
#     if iso_tz_info[0]=='-':
#         todo

#     pytz.common_timezones + pytz.all_timezones


def timestamp_int_to_tz_aware_datetime(timestamp, zone_name: str):
    dt = datetime.datetime.fromtimestamp(int(timestamp))
    zone = pytz.timezone(zone_name)
    return zone.localize(dt)


# def timestamp_zoned_str_to_tz_aware_datetime(timestamp, formats=None, dt_format=""):

#     formats = formats or [dt_format]

#     for dt_format in formats:
#         assert dt_format, ""
#         try:
#             dt = datetime.datetime.strptime(timestamp, dt_format)
#         except:
#             continue
#         else:
#             return zone.localize(dt)
#     assert False, "No matching dt format"


# for c in "+-":
#     if c in timestamp:
#         parts = timestamp.split(c)
#         pure_dt_string = parts[0]
#         zone = f"{c}{parts[1]}"
#         return timestamp_str_to_tz_aware_datetime(
#             timestamp=pure_dt_string,
#             zone_name=zone,
#             formats=formats,
#             dt_format=dt_format,
#         )

# raise Exception(
#     f"invalid timestamp string {timestamp}. Expected to see one of {c} to designate timezone"
# )


def timestamp_str_to_tz_aware_datetime(
    timestamp: str, zone_name: str, formats=None, dt_format=""
):
    formats = formats or [dt_format]
    zone = pytz.timezone(zone_name)

    for dt_format in formats:
        assert dt_format, ""
        try:
            dt = datetime.datetime.strptime(timestamp, dt_format)
        except:
            continue
        else:
            return zone.localize(dt)
    assert False, "No matching dt format"
