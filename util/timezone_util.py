from datetime import datetime
from zoneinfo import available_timezones, ZoneInfo

from persistence.model.user_model import TimeZoneInformation


def format_offset(seconds_offset: int) -> str:
    hours = seconds_offset // 3600
    minutes = abs(seconds_offset % 3600) // 60
    return f"{hours:+03}:{minutes:02}"


def generate_timezones():
    now = datetime.utcnow()
    timezones = []

    for tz_name in sorted(available_timezones()):
        try:
            tz = ZoneInfo(tz_name)
            offset = tz.utcoffset(now)
            if offset is None:
                continue
            offset_seconds = int(offset.total_seconds())
            timezones.append(TimeZoneInformation(time_zone=tz_name,
                                                 time_offset=offset_seconds,
                                                 time_offset_str=format_offset(offset_seconds)))
        except Exception as e:
            continue  # Skip problematic zones (very rare)
    return timezones


if __name__ == "__main__":
    tz_list = generate_timezones()
    [print(tz) for tz in tz_list]
