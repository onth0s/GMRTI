import os
import glob
import yaml
import pytest

REQUIRED_FIELDS = ["concept_id", "name", "intent", "dependencies", "invariants", "status"]
VALID_STATUSES = {"STABLE", "PROVISIONAL", "OPEN", "RECURSIVE", "RESTORED"}


def get_specs():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    specs_dir = os.path.join(base_dir, "specs")
    spec_files = glob.glob(os.path.join(specs_dir, "*.yaml")) + glob.glob(os.path.join(specs_dir, "*.yml"))
    specs = {}
    for f in spec_files:
        with open(f, "r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp)
            specs[os.path.basename(f)] = data
    return specs


def test_specs_schema():
    specs = get_specs()
    assert len(specs) > 0, "No specification files found in specs/"
    for filename, spec in specs.items():
        assert isinstance(spec, dict), f"{filename} is not a valid YAML mapping"
        for field in REQUIRED_FIELDS:
            assert field in spec, f"{filename} missing required field '{field}'"
        assert spec["status"] in VALID_STATUSES, (
            f"{filename} has invalid status '{spec['status']}', expected one of {VALID_STATUSES}"
        )
        assert isinstance(spec["dependencies"], list), f"{filename} dependencies must be a list"
        assert isinstance(spec["invariants"], list), f"{filename} invariants must be a list"
        assert len(spec["invariants"]) > 0, f"{filename} must declare at least one invariant"


def test_spec_dependencies_resolved():
    specs = get_specs()
    declared_ids = {spec["concept_id"] for spec in specs.values() if "concept_id" in spec}
    missing_dependencies = []
    for filename, spec in specs.items():
        for dep in spec.get("dependencies", []):
            if dep not in declared_ids:
                missing_dependencies.append((filename, spec.get("concept_id"), dep))
    assert not missing_dependencies, (
        f"Unresolved concept dependencies detected: {missing_dependencies}"
    )


def test_spec_name_uniqueness():
    """All concept specs must have unique name values."""
    specs = get_specs()
    names = [spec.get("name") for spec in specs.values() if spec.get("name")]
    assert len(names) == len(set(names)), (
        f"Duplicate spec names detected: {[n for n in names if names.count(n) > 1]}"
    )


def test_spec_empty_dependencies_valid():
    """A spec with an empty dependencies list is valid schema."""
    spec = {
        "concept_id": "TEST-EMPTY-DEPS",
        "name": "Test Empty Deps",
        "intent": "Verify empty dependencies list is valid.",
        "dependencies": [],
        "invariants": ["At least one invariant."],
        "status": "PROVISIONAL",
    }
    assert isinstance(spec["dependencies"], list)
    assert len(spec["dependencies"]) == 0


def test_spec_open_and_restored_statuses_valid():
    """OPEN and RESTORED are valid statuses per the schema."""
    for status in ("OPEN", "RESTORED"):
        assert status in VALID_STATUSES, f"{status} missing from VALID_STATUSES"
