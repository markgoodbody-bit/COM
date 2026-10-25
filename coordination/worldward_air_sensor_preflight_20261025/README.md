# A small air-sensor CSV preflight, not an air-quality verdict

**Independent, unreleased worldward source candidate — 25 October 2026.**

## The problem / stronger owners

Volunteers with inexpensive PM2.5 sensors may bring a spreadsheet to a local air-quality discussion. A plausible-looking number is not necessarily a trustworthy time series: missing clock offsets, duplicate instants, irregular sampling and blank or invalid readings can disappear in a simple graph. This tool tests **only those narrow structural defects** on one locally supplied two-column CSV. It does not validate the sensor or interpret pollution. A local air-quality professional, community monitoring network, or calibrated reference measurement remains a stronger owner of any environmental finding.

For London, **Breathe London** provides a real sensor network with established CERC quality assurance, quality control and calibration. It already supplies 1-minute readings aggregated to hourly data; do not replace or reprocess its existing accepted methodology with this tool. DEFRA's Air Quality Expert Group warns that low-cost sensor accuracy may be affected by humidity, temperature and interfering pollutants, and such devices are not direct substitutes for reference monitors. The US EPA's *Enhanced Air Sensor Guidebook* explains sensor planning, interpretation and communication. These are technical sources, not endorsements of this little program.

**Primary sources checked 25 October 2026** (not live sensor measurements):

- DEFRA AQEG, uncertainty: https://uk-air.defra.gov.uk/research/aqeg/pollution-sensors/understanding-uncertainties.php
- DEFRA AQEG, when a sensor is appropriate: https://uk-air.defra.gov.uk/research/aqeg/pollution-sensors/how-could-I-use.php
- Breathe London network/calibration: https://www.breathelondon.org/our-sensor-network
- Breathe London CSV availability/cadence context: https://www.breathelondon.org/sensors/join-the-breathe-london-network
- US EPA air sensor guidebook: https://www.epa.gov/air-sensor-toolbox/how-use-air-sensors-air-sensor-guidebook

## What this adds

A reproducible **local-only** check before treating a spreadsheet as evidence. It does not require an account, upload, data service, API key, network access or nonstandard Python library; it does not collect addresses or identifiers. Input has exactly two columns:

```csv
timestamp,pm25_ug_m3
2026-10-25T00:00:00Z,8
2026-10-25T01:00:00Z,9
2026-10-25T03:00:00Z,11
```

`timestamp` is ISO 8601 **including `Z` or an explicit numeric timezone offset**. This disambiguates the repeated autumn clock-change hour; a local timestamp without an offset is rejected, not guessed. `pm25_ug_m3` is a **user-declared** concentration in micrograms per cubic metre. The program cannot independently establish the real unit or pollutant. Export data from only **one** sensor; do not merge different instruments into one file. Remove names, locations, IDs and any personal data before preparing this narrow two-column CSV. Convert units/timestamps against the actual device documentation: never guess or silently change them to fit the script.

Run with Python **3.11 or newer**:

```bash
python3 air_sensor_preflight.py sample_synthetic_pm25.csv --interval-minutes 60
```

The explicit `--interval-minutes 60` asserts a continuously expected hourly cadence **between the first and last timestamps**. If the true sampling schedule is unknown, **omit the argument**; gap counting will say `NOT_ASSESSED` instead of inventing missing measurements. Any apparent gaps may reflect intentionally stopped sampling or a change in reporting schedule, not faulty equipment. The sample has a deliberate two-hour gap, so it returns `REVIEW` with **one potential unobserved slot**. Exit codes: `0` structurally clean, `1` review structural warnings, `2` structural failure. Output is JSON to stdout with issue codes and row numbers; it does not print the original concentration values. A `PASS` is **not** an air-safety verdict.

Tests, all synthetic/offline:

```bash
python3 -m unittest discover -s . -p 'test_air_sensor_preflight.py' -v
```

Boundary: UTF-8 or UTF-8 BOM input, max 2 MiB, max 100,000 records, exact header names; reject extra columns instead of accidentally processing private fields. The report includes a SHA-256 of the entire accepted-size input so someone can tell if the data changed, not a public publication receipt. Oversized input does **not** claim a SHA-256 of an unread tail.

## What has **not** been validated

There is **no real sensor dataset, no calibration or reference comparison, no humidity/siting correction, no NO2 calculation, no statistical exposure analysis, no resident or expert trial, no accessibility study, and no deployment**. Neither a structural `PASS` nor a low reported concentration demonstrates health safety, compliance or an absence of local problems. This program does not set thresholds or recommend behaviour. The **source can be retired** if Breathe London/DEFRA specialists find the workflow misleads people, a real export disproves the assumptions, or established network QA already covers the entire use case more reliably and accessibly.

To have practical value, a real volunteer or qualified air-quality specialist would need to try this on a deliberately shared, non-sensitive, correctly documented sensor export, check the diagnostics and decide whether the tool makes their work clearer. That invitation/testing decision belongs to a real human owner; no one was contacted for this draft.
