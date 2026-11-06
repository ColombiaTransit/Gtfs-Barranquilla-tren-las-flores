# Tren Turístico Las Flores – Barranquilla (GTFS)

Static GTFS Schedule feed for the tourist tram between **Estación Las Flores** and **Estación Puerto Mocho**, Barranquilla, Colombia.

## Data quality
This is an **experimental, assumption-based timetable**, not an official departure schedule. A visitor video reports a 20-minute headway; Quilla Life reports a 7–10 minute journey. Two vehicles are assumed to operate concurrently, using the passing loop mapped in OpenStreetMap. Actual dispatch times and the first return departures have not been independently verified.

- Tue–Fri: model departures 10:00–16:40, every 20 minutes in each direction.
- Sat/Sun: model departures 08:00–16:40, every 20 minutes in each direction.
- Monday: normally closed; Colombian Monday holidays are modeled as weekend service, with the following Tuesday closed for maintenance.
- Travel time: 10 minutes in either direction.
- The published 17:30 final return from Puerto Mocho is **not yet reconciled** with the regular 20-minute grid and is therefore not represented as a confirmed departure.
- Service calendar is regenerated through the end of the following year.

These assumptions may change after an official timetable is found. The feed does not assert that every model trip actually operates.

## Sources
- [Municipality: infrastructure and vehicles](https://barranquilla.gov.co/mi-barranquilla/listo-el-tren-de-las-flores-pronto-rodara-hasta-la-playa-de-puerto-mocho-alcalde-char)
- [TaQui: opening hours, Monday holiday maintenance, final return](https://www.taqui-co.com/trenpuertomocho)
- [Quilla Life: approximate travel time](https://quillalife.com/experiencias/tren-turistico-las-flores/)
- [Visitor video: reported 20-minute headway](https://www.tiktok.com/@viajandosinbarreras/video/7570492238229277973)
- OpenStreetMap Overpass export (2026-11-06), ODbL. Geometry stored in `data/railway.geojson`.

## Build
```bash
python -m pip install -r requirements.txt
python scripts/build_gtfs.py
```
The output is `dist/gtfs.zip`. A GitHub Actions workflow builds, validates and uploads the feed as an artifact. Publication to a release is a separate step after successful validation.

## Maintenance
Review the operating hours, headways, station coordinates and source pages a few times a year. Do not scrape sources on each build.
