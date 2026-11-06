# Tren Turístico Las Flores – Barranquilla

Experimental, assumption-based static GTFS feed for the Las Flores–Puerto Mocho tourist tram.

**Important:** departure times are modeled, not an official published timetable. The 20-minute headway is based on a visitor report, and the 10-minute travel time is based on Quilla Life. Two concurrently operating trains are assumed. The TaQui-reported last return at 17:30 remains unresolved and is not included in the model.

## Build

```sh
pip install -r requirements.txt
python scripts/build_gtfs.py
```

Run the `Build and validate GTFS` GitHub Action to generate `gtfs.zip` and run MobilityData validation. Download the workflow artifact after the run succeeds.

See [research register](docs/research-register.md) for sources, verification status and open issues. Review the mostly static source data a few times per year.

## Sources

- [Municipality](https://barranquilla.gov.co/mi-barranquilla/listo-el-tren-de-las-flores-pronto-rodara-hasta-la-playa-de-puerto-mocho-alcalde-char)
- [TaQui](https://www.taqui-co.com/trenpuertomocho)
- [Quilla Life](https://quillalife.com/experiencias/tren-turistico-las-flores/)
- [Visitor video](https://www.tiktok.com/@viajandosinbarreras/video/7570492238229277973)
- OSM geometry (ODbL), retrieved 2026-11-06.
