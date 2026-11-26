import glob
import os
import re
import pytest
import yaml

REQUIRED_FIELDS = [
    "concept_id",
    "name",
    "intent",
    "dependencies",
    "invariants",
    "status",
    "last_modified",
]
VALID_STATUSES = {"STABLE", "PROVISIONAL", "OPEN", "RECURSIVE", "RESTORED"}

# Intentional co-definitional cycles between mutually dependent core concepts.
ALLOWLISTED_CYCLE_SETS = {
    frozenset({"GMRTI-COMOSI", "GMRTI-ENTROPY", "GMRTI-OPERATIONAL-ACTION-THRESHOLD"}),
    frozenset({"GMRTI-COMOSI", "GMRTI-OPERATIONAL-ACTION-THRESHOLD"}),
}


@pytest.fixture(scope="session")
def specs():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    specs_dir = os.path.join(base_dir, "specs")
    spec_files = glob.glob(os.path.join(specs_dir, "*.yaml")) + glob.glob(
        os.path.join(specs_dir, "*.yml")
    )
    loaded = {}
    for f in spec_files:
        with open(f, "r", encoding="utf-8") as fp:
            loaded[os.path.basename(f)] = yaml.safe_load(fp)
    return loaded


def validate_spec(filename: str, spec: dict) -> None:
    assert isinstance(spec, dict), f"{filename} is not a valid YAML mapping"
    for field in REQUIRED_FIELDS:
        assert field in spec, f"{filename} missing required field '{field}'"
    assert spec["status"] in VALID_STATUSES, (
        f"{filename} has invalid status '{spec['status']}', expected one of {VALID_STATUSES}"
    )
    assert isinstance(spec["dependencies"], list), f"{filename} dependencies must be a list"
    assert isinstance(spec["invariants"], list), f"{filename} invariants must be a list"
    assert len(spec["invariants"]) > 0, f"{filename} must declare at least one invariant"
    if "open_issues" in spec:
        assert isinstance(spec["open_issues"], list), f"{filename} open_issues must be a list"


def test_specs_schema(specs):
    assert len(specs) > 0, "No specification files found in specs/"
    for filename, spec in specs.items():
        validate_spec(filename, spec)


def test_spec_dependencies_resolved(specs):
    declared_ids = {spec["concept_id"] for spec in specs.values() if "concept_id" in spec}
    missing_dependencies = []
    for filename, spec in specs.items():
        for dep in spec.get("dependencies", []):
            if dep not in declared_ids:
                missing_dependencies.append((filename, spec.get("concept_id"), dep))
    assert not missing_dependencies, (
        f"Unresolved concept dependencies detected: {missing_dependencies}"
    )


def test_spec_dependency_cycles_allowlisted(specs):
    """Only explicitly allowlisted co-definitional cycles may exist in specs/."""
    adj = {
        spec["concept_id"]: list(spec.get("dependencies", []))
        for spec in specs.values()
        if "concept_id" in spec
    }
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in adj}
    unexpected_cycles = []

    def dfs(u, path):
        color[u] = GRAY
        for v in adj.get(u, []):
            if v not in color:
                continue
            if color[v] == GRAY:
                cycle = path[path.index(v):]
                if frozenset(cycle) not in ALLOWLISTED_CYCLE_SETS:
                    unexpected_cycles.append(cycle + [v])
            elif color[v] == WHITE:
                dfs(v, path + [v])
        color[u] = BLACK

    for node in adj:
        if color[node] == WHITE:
            dfs(node, [node])

    assert not unexpected_cycles, f"Unexpected spec dependency cycles: {unexpected_cycles}"


def test_spec_name_uniqueness(specs):
    """All concept specs must have unique name values."""
    names = [spec.get("name") for spec in specs.values() if spec.get("name")]
    assert len(names) == len(set(names)), (
        f"Duplicate spec names detected: {[n for n in names if names.count(n) > 1]}"
    )


def test_spec_concept_id_naming_convention(specs):
    """All concept_ids must follow the GMRTI-* naming convention."""
    for filename, spec in specs.items():
        concept_id = spec.get("concept_id", "")
        assert concept_id.startswith("GMRTI-"), (
            f"{filename}: concept_id '{concept_id}' does not start with 'GMRTI-'"
        )
        assert concept_id == concept_id.upper(), (
            f"{filename}: concept_id '{concept_id}' must be uppercase"
        )


def test_spec_filename_slug_matches_concept_id(specs):
    """Each spec's filename (concept_<slug>.yaml) must match GMRTI-<SLUG>."""
    for filename, spec in specs.items():
        base = filename
        for ext in (".yaml", ".yml"):
            if base.endswith(ext):
                base = base[:-len(ext)]
        assert base.startswith("concept_"), f"Spec file '{filename}' does not start with 'concept_'"
        slug = base[len("concept_"):].replace("_", "-").upper()
        expected_id = f"GMRTI-{slug}"
        assert spec.get("concept_id") == expected_id, (
            f"{filename}: expected concept_id '{expected_id}', got '{spec.get('concept_id')}'"
        )


def test_spec_last_modified_date_format(specs):
    """All specs must declare last_modified in YYYY-MM-DD ISO format."""
    for filename, spec in specs.items():
        last_modified = str(spec.get("last_modified", ""))
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", last_modified), (
            f"{filename}: invalid last_modified date format '{last_modified}', expected YYYY-MM-DD"
        )
