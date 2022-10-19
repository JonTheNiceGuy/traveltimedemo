import q
import os
import csv
import sys
import yaml
import dateparser
import traveltimepy
from os import walk
from datetime import datetime
from humanfriendly import format_timespan

def dict_reorder(item):
    return {k: dict_reorder(v) if isinstance(v, dict) else v for k, v in sorted(item.items())}

def tagwalk(tags, people):
    data = []
    my_tags = []
    for tag in tags:
        my_tags.append(tag)

    for tag in tags:
        if 'M-' in tag[0:2]:
            manager = tag[2:]
            if manager in people.keys():
                m_tags = tagwalk(people[manager]["tags"], people)
                my_tags += m_tags
    for tag in my_tags:
        if tag not in data:
            data.append(tag)
    return data

def write_output(writer, destinations, output, all_tags):
    result_output = ["Alias"]
    result_counter = 0
    result_counter_output = []
    result_times_output = []
    for destination in destinations:
        result_output += [destination]
        result_counter = result_counter+1
        result_counter_output += [f'result{str(result_counter).zfill(2)}']
        result_times_output += [f'result{str(result_counter).zfill(2)}_Time']
    for tag in sorted(all_tags):
        result_output += [f'Tag: {tag}']
    writer.writerow(result_output)

    sorted_output = dict(sorted(output.items()))
    for person in sorted_output:
        person_data = sorted_output[person]
        result_output = [person]
        result_counter = 0
        result_counter_output = []
        result_times_output = []
        for destination in destinations:
            result_counter = result_counter+1
            if destination in person_data:
                result_output += [person_data[destination] or ""]
            else:
                result_output += [len(destinations)+1]
            if f'result{str(result_counter).zfill(2)}' in person_data:
                result_counter_output += [person_data[f"result{str(result_counter).zfill(2)}"] or ""]
            else:
                result_counter_output += ['']
            if f'result{str(result_counter).zfill(2)}Time' in person_data:
                result_times_output += [person_data[f"result{str(result_counter).zfill(2)}Time"] or ""]
            else:
                result_times_output += ['']
        for tag in sorted(all_tags):
            if tag in person_data["tags"]:
                result_output += [tag]
            else:
                result_output += [""]
        writer.writerow(result_output)

with open("/input/cities.yml", "r") as stream:
    try:
        city_locations = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

if "DEBUG_STUFF" in os.environ and os.environ["DEBUG_STUFF"] != '':
    print(city_locations)

destinations = []
for location in city_locations:
    destinations.append(location["id"])

people = {}
for (dirpath, dirnames, filenames) in walk("/input/people/"):
    for this_filename in filenames:
        if this_filename.lower()[-3:] == "yml" or this_filename.lower()[-4] == "yaml":
        with open(dirpath + this_filename, "r") as stream:
            try:
                people = people | yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                exit(1)

groups = {}
for (dirpath, dirnames, filenames) in walk("/input/groups/"):
    for this_filename in filenames:
        if this_filename.lower()[-3:] == "yml" or this_filename.lower()[-4] == "yaml":
        with open(dirpath + this_filename, "r") as stream:
            try:
                group_data = yaml.safe_load(stream)
                q(group_data)
                groups = groups | group_data
            except yaml.YAMLError as exc:
                print(exc)
                exit(1)

with open("/input/postcode-outcodes.csv", "r") as stream:
    try:
        csv_stream = csv.reader(stream)
        outcodes = [row for row in csv_stream]
    except csv.Error as exc:
        print(exc)
        exit(1)

all_tags = []
people_locations = []
for person_id in people:
    person = people[person_id]

    if "tags" not in person:
        person["tags"] = []

    for group in groups:
        if person_id in groups[group]:
            person["tags"] += [group]

    person["mytags"] = tagwalk(person["tags"], people)

    if (
        (
            "TAG" not in os.environ and "MTAG" not in os.environ
        ) or (
            "TAG" in os.environ and os.environ["TAG"] != '' and os.environ["TAG"] in person["mytags"]
        ) or (
            "MTAG" in os.environ and os.environ["MTAG"] != '' and (
                f'M-{os.environ["MTAG"]}' in person["mytags"] or
                os.environ["MTAG"] == person_id
            )
        )
    ):
        person["id"] = person_id
        postcode = person["postcode"].upper()
        if "coords" not in person and "postcode" in person:
            for outcode in outcodes:
                if outcode[0] == postcode:
                    person["coords"] = {}
                    person["coords"]["lat"] = float(outcode[1])
                    person["coords"]["lng"] = float(outcode[2])

        for tag in person["mytags"]:
            if tag not in all_tags:
                all_tags.append(tag)

        people_locations.append(person)

if "DEBUG_STUFF" in os.environ and os.environ["DEBUG_STUFF"] != '':
    print(people_locations)
    print(sorted(all_tags))
    exit(1)

the_time = datetime.utcnow()
if "TRAVELTIME_OFFSET" in os.environ:
    timezone = "Europe/London"
    if "TZ" in os.environ:
        timezone = os.environ["TZ"]
    the_time = dateparser.parse(
        os.environ["TRAVELTIME_OFFSET"], settings={'TIMEZONE': timezone})

departure_time = the_time.isoformat()

output = {}

for person in people_locations:
    departure_search = {
        "id": person["id"],
        "departure_location_id": person["id"],
        "arrival_location_ids": destinations,
        "transportation": {"type": "public_transport"},
        "departure_time": departure_time,
        "travel_time": (60*60)*4, # Four Hours
        "properties": ["travel_time", "route"],
        "range": { # Range of starting time before and after the "departure time"
            "enabled": True,
            "width": 3600, # One Hour
            "max_results": 1
        }
    }
    out = traveltimepy.time_filter(
        locations=city_locations + people_locations,
        departure_searches=departure_search
    )

    all_results = {}

    for result in out["results"]:
        for location in result["locations"]:
            id = location["id"]
            ttime = 9999
            atime = 0
            dtime = 0
            for properties in location["properties"]:
                this_atime = properties["route"]["arrival_time"]
                this_dtime = properties["route"]["departure_time"]
                this_ttime = properties["travel_time"]
                if this_ttime < ttime:
                    ttime = this_ttime
                    atime = this_atime
                    dtime = this_dtime
            if ttime < 9999:
                all_results[str(ttime).zfill(5)] = {
                    "destination": id,
                    "arrivalTime": atime,
                    "departureTime": dtime,
                    "travelTime": format_timespan(ttime, max_units=2)
                }
    sorted_results = dict(sorted(all_results.items()))
    slot = 0
    output[person["id"]] = {"tags": person["mytags"]}
    for result in sorted_results:
        slot = slot+1
        result_data = sorted_results[result]
        output[person["id"]
               ][f'result{str(slot).zfill(2)}'] = result_data["destination"]
        output[person["id"]][result_data["destination"]] = slot
        output[person["id"]
               ][f'result{str(slot).zfill(2)}Time'] = result_data["travelTime"]

output_file = sys.stdout
if "OUTPUT_FILE" in os.environ and os.environ["OUTPUT_FILE"] != '':
    output_file = f'/output/{os.environ["OUTPUT_FILE"]}'
    with open(output_file, "wt") as fp:
        writer = csv.writer(fp, delimiter=",", quoting=csv.QUOTE_ALL)
        write_output(writer, destinations, output, all_tags)
else:
    writer = csv.writer(sys.stdout, delimiter=",", quoting=csv.QUOTE_ALL)
    write_output(writer, destinations, output, all_tags)

