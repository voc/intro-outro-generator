from schedulelib_xml import events_from_xml_schedule
from schedulelib_json import events_from_json_schedule


def events(schedule_url):
    print(f"Downloading schedule from URL: {schedule_url}")
    if schedule_url.endswith(".xml"):
        return events_from_xml_schedule(schedule_url)
    if schedule_url.endswith(".json"):
        return events_from_json_schedule(schedule_url)
    raise ValueError(
        f"schedulelib.events(): could not determine whether {schedule_url!r} is XML or JSON"
    )
