"""Validate the proposed edge message schema against the contract fixtures.

Every file in ``testing/fixtures/contracts/valid`` must validate, and every file in
``testing/fixtures/contracts/invalid`` must be rejected. Add a fixture whenever the
contract in ``docs/api/contracts.md`` changes.
"""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "docs" / "api" / "schemas" / "edge-messages.v0.schema.json"
FIXTURES = REPO_ROOT / "testing" / "fixtures" / "contracts"

VALID = sorted((FIXTURES / "valid").glob("*.json"))
INVALID = sorted((FIXTURES / "invalid").glob("*.json"))


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def validator() -> Draft202012Validator:
    return Draft202012Validator(_load(SCHEMA_PATH))


def test_schema_is_valid_json_schema() -> None:
    Draft202012Validator.check_schema(_load(SCHEMA_PATH))


def test_fixtures_exist() -> None:
    assert VALID, "expected at least one valid contract fixture"
    assert INVALID, "expected at least one invalid contract fixture"


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.stem)
def test_valid_fixture_is_accepted(validator: Draft202012Validator, path: Path) -> None:
    errors = [e.message for e in validator.iter_errors(_load(path))]
    assert errors == []


@pytest.mark.parametrize("path", INVALID, ids=lambda p: p.stem)
def test_invalid_fixture_is_rejected(validator: Draft202012Validator, path: Path) -> None:
    assert not validator.is_valid(_load(path))
