import sys
import platform
import sys
import platform

def test_os_is_linux():
    assert platform.system().lower() == "linux", f"Test failed: OS is {platform.system()}, expected Linux"
