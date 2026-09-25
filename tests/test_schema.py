"""Validate the Triton observation schema and its examples."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "observation.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

VALID = sorted((ROOT / "examples" / "valid").glob("*.json"))
INVALID = sorted((ROOT / "examples" / "invalid").glob("*.json"))


def test_schema_is_valid_draft_2020_12():
    Draft202012Validator.check_schema(SCHEMA)


def test_examples_exist():
    assert VALID, "expected at least one valid example"
    assert INVALID, "expected at least one invalid example"


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.name)
def test_valid_examples_pass(path):
    errors = list(VALIDATOR.iter_errors(json.loads(path.read_text())))
    assert not errors, [e.message for e in errors]


@pytest.mark.parametrize("path", INVALID, ids=lambda p: p.name)
def test_invalid_examples_fail(path):
    errors = list(VALIDATOR.iter_errors(json.loads(path.read_text())))
    assert errors, f"{path.name} should fail validation"
