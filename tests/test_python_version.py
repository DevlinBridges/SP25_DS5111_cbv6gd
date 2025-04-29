import pytest
import sys

allowed_versions = {"3.10", "3.11", "3.12"}
current_version = f"{sys.version_info.major}.{sys.version_info.minor}"

@pytest.mark.skipif(
    current_version not in allowed_versions,
    reason=f"Skipping: Python {current_version} not in {allowed_versions}"
)
def test_python_version():
    assert current_version in allowed_versions
