from requests import get

from schedulelib_xml import events_from_xml_schedule
from schedulelib_json import events_from_json_schedule


def _from_url(schedule_url):
    print(f"Downloading schedule from URL: {schedule_url}")
    r = get(schedule_url, timeout=10)
    r.raise_for_status()
    return r.text


def _from_file(schedule_url):
    print(f"Using locally available schedule {schedule_url}")
    with open(schedule_url) as f:
        return f.read()


def events(schedule_url, **kwargs):
    if schedule_url.startswith("file://"):
        schedule_url = schedule_url[7:]

    if "://" in schedule_url:
        schedule_text = _from_url(schedule_url)
    else:
        schedule_text = _from_file(schedule_url)

    if schedule_url.endswith(".xml"):
        return events_from_xml_schedule(schedule_text, **kwargs)
    if schedule_url.endswith(".json"):
        return events_from_json_schedule(schedule_text)
    raise ValueError(
        f"schedulelib.events(): could not determine whether {schedule_url!r} is XML or JSON"
    )
