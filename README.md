# Triton Observation Schema

[![validate](https://github.com/Triton-Ocean-Systems/triton-observation-schema/actions/workflows/validate.yml/badge.svg)](https://github.com/Triton-Ocean-Systems/triton-observation-schema/actions/workflows/validate.yml)
![status](https://img.shields.io/badge/status-draft%20v0.1-0a2a43)
![license](https://img.shields.io/badge/license-Apache--2.0-0a2a43)

An open JSON Schema for ocean observation records that carry their own provenance.

Ocean data is hard to trust and hard to combine. Measurements arrive without a clear record of which platform produced them, when and where, which sensor was used, when it was last calibrated, whether it passed quality checks, or how a derived value was computed. This schema makes those facts part of every record.

It is the record format Triton Ocean Systems is designing for data from its BeachNode, OceanNode and SailNode platforms and for the external feeds shown in Triton SEAVANT. We publish it openly so partners, researchers and agencies can read, validate and exchange the same data.

> **Status: draft v0.1.** The format may change before v1.0. Feedback is welcome through issues.

## What a record contains

| Field | Purpose |
|---|---|
| `observation_id` | Globally unique ID (UUID) |
| `node` | Which platform produced it (`node_id`, `node_type`, firmware) |
| `observed_at` / `received_at` | Measurement and arrival time, RFC 3339 in UTC |
| `location` | Latitude, longitude, depth (m, positive down), position source and accuracy |
| `sensor` | Sensor ID, manufacturer, model, serial |
| `variable` | Variable name, optional [CF standard name](https://cfconventions.org/), unit in [UCUM](https://ucum.org/) |
| `value` / `uncertainty` | The measurement and its standard uncertainty |
| `quality` | [IOOS QARTOD](https://ioos.noaa.gov/project/qartod/) flag and the tests applied |
| `calibration` | When and how the sensor was last calibrated |
| `lineage` | Raw, derived or aggregated; source observation IDs; software and version; raw payload hash |

Derived and aggregated records must list the observations they were computed from, so any value can be traced back to raw measurements.

## Example

```json
{
  "schema_version": "0.1.0",
  "observation_id": "3f1c2a9e-7b4d-4c1e-9a0f-2d6b8e5c1a70",
  "node": { "node_id": "beachnode-example-01", "node_type": "beachnode" },
  "observed_at": "2026-09-24T14:00:00Z",
  "location": { "latitude": 26.0112, "longitude": -80.1156, "depth_m": 0.5, "position_source": "fixed_survey" },
  "sensor": { "sensor_id": "temp-01" },
  "variable": { "name": "water_temperature", "cf_standard_name": "sea_water_temperature", "unit": "Cel" },
  "value": 29.4,
  "quality": { "flag": 1, "tests_applied": ["gross_range", "spike"] },
  "lineage": { "processing_level": "raw", "software": { "name": "node-firmware", "version": "0.1.0" } }
}
```

More examples, including records that are expected to fail, are in [`examples/`](examples/). Example values are illustrative, not real measurements.

## Validate a record

```bash
pip install -r requirements-dev.txt
pytest -v
```

Or in your own code:

```python
import json
from jsonschema import Draft202012Validator, FormatChecker

schema = json.load(open("schema/observation.schema.json"))
validator = Draft202012Validator(schema, format_checker=FormatChecker())
validator.validate(json.load(open("my-record.json")))
```

## Layout

```
schema/observation.schema.json   JSON Schema (draft 2020-12)
examples/valid/                  records that must validate
examples/invalid/                records that must fail
tests/                           automated checks run on every push
```

## License

Apache License 2.0. See [LICENSE](LICENSE).

---

Maintained by [Triton Ocean Systems](https://github.com/Triton-Ocean-Systems).
