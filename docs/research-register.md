# Research register

Last source review: 2026-11-06. All timetable assumptions below require field verification.

| Fact | Value | Evidence | Status |
| --- | --- | --- | --- |
| Stations | Las Flores, Puerto Mocho | Municipality and OSM ways 1295487575, 1295487580 | Confirmed names; stop coordinates approximated |
| Track | Predominantly single-track, with passing loop | OSM ways 1295487570 and 1295487571 | Mapped |
| Vehicles | Mar and Río, 70 seats each | Municipality | Official announcement |
| Concurrent operation | Both vehicles run simultaneously | Project assumption | Unverified |
| Running time | 7–10 minutes | Quilla Life | Secondary report; model uses 10 min |
| Headway | 20 minutes | TikTok video reported by project contributor | Secondary; model assumption |
| Opening hours | Tue–Fri 10:00–17:00; weekends and holidays 08:00–17:00 | TaQui | Published, currency not verified |
| Monday holiday | Operates, with Tuesday maintenance closure | TaQui | Published, currency not verified |
| Last return | 17:30 from Puerto Mocho | TaQui | Published; included as an additional one-way trip on all operating days |
| Fare | COP 10,000 return | TaQui | Historical published figure, not included in GTFS |

## Holiday modeling decision (2026-11-06)
All Colombian public holidays use the existing weekend departure pattern (08:00 start, assumed 20-minute interval), because no separate holiday frequency data is available. Holidays falling on Tue–Fri replace weekday service; holiday Mondays activate weekend service. The Tuesday following a holiday Monday is excluded for maintenance. This is an explicit timetable modeling assumption, not a verified holiday timetable.

The route is encoded as standard tram (`route_type=0`) with short name `TLF`.

## Open issues
1. Confirm first departures and whether the published 17:30 final return operates every service day. The 17:30 return is explicitly included outside the assumed 20-minute grid.
2. Verify exact platform boarding points and stop coordinates.
3. Verify simultaneous two-vehicle service and passing loop usage.
4. Verify current ticketing and holiday operations.
5. Replace simplified centerline with complete original OSM geometry when appropriate.

The timetable is illustrative and is not an official operating schedule.
