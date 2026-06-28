from requests import get


def events_from_json_schedule(schedule_url):
    r = get(schedule_url, timeout=10)
    r.raise_for_status()
    schedule = r.json()

    for day in schedule["schedule"]["conference"]["days"]:
        for room_name, room in day["rooms"].items():
            for talk in room:
                persons = [person["name"] for person in talk.get("persons", [])]

                yield {
                    "day": day["index"],
                    "id": talk["id"],
                    "title": talk["title"],
                    "subtitle": talk["subtitle"],
                    "persons": persons,
                    "personnames": ", ".join(persons),
                    "room": room_name,
                    "track": talk["track"],
                    "url": talk["url"],
                }
