import sys


def test_python_version():
    allowed_versions = {"3.10", "3.11", "3.12"}
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}"

    assert (
        current_version in allowed_versions
    ), f"Test failed: Python {current_version} is not in {allowed_versions}"
