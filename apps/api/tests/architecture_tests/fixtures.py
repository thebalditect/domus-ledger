import pytest
from pathlib import Path
from pytestarch import get_evaluable_architecture as getarch, EvaluableArchitecture


@pytest.fixture
def get_evaluable_architecture() -> EvaluableArchitecture:

    root_parent_directory = Path(__file__).parent.parent.parent

    src_dir = root_parent_directory / "src"
    module_path = src_dir / "domus_ledger_api"
    print(f"source directory is {src_dir}")

    return getarch(root_path=str(src_dir), module_path=str(module_path))
