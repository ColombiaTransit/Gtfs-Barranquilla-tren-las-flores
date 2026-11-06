#!/usr/bin/env python3
"""Build an assumption-based static GTFS from reviewed local data."""
import csv
import io
import json
import math
import zipfile
from datetime import date, timedelta
from pathlib import Path
from holidays import country_holidays

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist" / "gtfs.zip"
TZ = "America/Bogota"

def csvbytes(fields, rows):
    f = io.StringIO(newline="")
    w = csv.writer(f, lineterminator="\n")
    w.writerow(fields)
    w.writerows(rows)
    return f.getvalue().encode("utf-8")

def clock(minute):
    return f"{minute//60:02d}:{minute%60:02d}:00"

def dist(a,b):
    lon1,lat1=map(math.radians,a)
    lon2,lat2=map(math.radians,b)
    x=math.sin((lat2-lat1)/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
    return 6371000*2*math.asin(math.sqrt(x))

def main():
    data=json.loads((ROOT/"data"/"railway.geojson").read_text())
    coords=data["features"][0]["geometry"]["coordinates"]
    stops=[("LF","Estación Las Flores",11.04599,-74.83004),("PM","Estación Puerto Mocho",11.06293,-74.84370)]
    # End-point distances are based on the OSM rail centerline, not direct aerial distance.
    cumulative=[0.0]
    for a,b in zip(coords,coords[1:]):
        cumulative.append(cumulative[-1]+dist(a,b))
    total=cumulative[-1]
    today=date.today()
    start=date(today.year,1,1)
    end=date(today.year+1,12,31)
    hol=country_holidays("CO",years=range(start.year,end.year+1))
    # Two calendars: Tue–Fri and weekends; public holidays use weekend hours.
    cal=[["weekday",0,1,1,1,1,0,0,start.strftime("%Y%m%d"),end.strftime("%Y%m%d")],
         ["weekend",0,0,0,0,0,1,1,start.strftime("%Y%m%d"),end.strftime("%Y%m%d")]]
    exceptions=[]
    d=start
    while d<=end:
        stamp=d.strftime("%Y%m%d")
        if d in hol:
            # Holidays use weekend opening hours; no separate frequency evidence.
            if d.weekday()<=4:
                exceptions.append(["weekend",stamp,1])
                if d.weekday()!=0:
                    exceptions.append(["weekday",stamp,2])
            if d.weekday()==0:
                # Tuesday following a holiday Monday is a maintenance closure.
                nxt=d+timedelta(days=1)
                if nxt<=end:
                    exceptions.append(["weekday",nxt.strftime("%Y%m%d"),2])
        d+=timedelta(days=1)
    routes=[["TLF","EDUBAR","TLF","Las Flores – Puerto Mocho",0]]
    trips=[]
    stop_times=[]
    # Two trains are modeled as simultaneous opposite-direction departures.
    # Departures are estimated, not officially published.
    for service,begin in [("weekday",600),("weekend",480)]:
        for minute in range(begin,1001,20):  # last 16:40
            for direction,(a,b) in enumerate([("LF","PM"),("PM","LF")]):
                trip=f"{service}_{minute}_{direction}"
                shape_id="TLF_MAIN" if direction==0 else "TLF_RETURN"
                trips.append(["TLF",service,trip,"Puerto Mocho" if direction==0 else "Las Flores",direction,shape_id])
                stop_times.extend([[trip,clock(minute),clock(minute),a,1,0],
                                   [trip,clock(minute+10),clock(minute+10),b,2,round(total,1)]])
    # Published final return from Puerto Mocho at 17:30 (TaQui).
    # This is an additional trip outside the assumed 20-minute departure grid.
    for service in ("weekday", "weekend"):
        trip=f"{service}_last_return_1730"
        trips.append(["TLF",service,trip,"Las Flores",1,"TLF_RETURN"])
        stop_times.extend([[trip,"17:30:00","17:30:00","PM",1,0],
                           [trip,"17:40:00","17:40:00","LF",2,round(total,1)]])
    shapes=[]
    for i,((lon,lat),m) in enumerate(zip(coords,cumulative)):
        shapes.append(["TLF_MAIN",lat,lon,i+1,round(m,1)])
    for i,((lon,lat),m) in enumerate(zip(reversed(coords),reversed(cumulative))):
        shapes.append(["TLF_RETURN",lat,lon,i+1,round(total-m,1)])
    files={
        "agency.txt":csvbytes(["agency_id","agency_name","agency_url","agency_timezone","agency_lang"],[["EDUBAR","EDUBAR S.A.","https://www.edubar.com.co/",TZ,"es"]]),
        "stops.txt":csvbytes(["stop_id","stop_name","stop_lat","stop_lon","location_type"],[[id,name,lat,lon,0] for id,name,lat,lon in stops]),
        "routes.txt":csvbytes(["route_id","agency_id","route_short_name","route_long_name","route_type"],routes),
        "calendar.txt":csvbytes(["service_id","monday","tuesday","wednesday","thursday","friday","saturday","sunday","start_date","end_date"],cal),
        "calendar_dates.txt":csvbytes(["service_id","date","exception_type"],exceptions),
        "trips.txt":csvbytes(["route_id","service_id","trip_id","trip_headsign","direction_id","shape_id"],trips),
        "stop_times.txt":csvbytes(["trip_id","arrival_time","departure_time","stop_id","stop_sequence","shape_dist_traveled"],stop_times),
        "shapes.txt":csvbytes(["shape_id","shape_pt_lat","shape_pt_lon","shape_pt_sequence","shape_dist_traveled"],shapes),
        "feed_info.txt":csvbytes(["feed_publisher_name","feed_publisher_url","feed_lang","feed_start_date","feed_end_date","feed_version"],[["ColombiaTransit","https://github.com/ColombiaTransit/Gtfs-Barranquilla-tren-las-flores","es",start.strftime("%Y%m%d"),end.strftime("%Y%m%d"),today.strftime("%Y%m%d")]]),
    }
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for name,body in files.items():
            z.writestr(name,body)
    print(f"Built {OUT}: {len(trips)} trips, {len(coords)} shape points, {total:.0f}m track")

if __name__=="__main__":
    main()
