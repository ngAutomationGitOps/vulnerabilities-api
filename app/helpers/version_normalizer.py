# utils.py
import re

def normalize_rpm_version(rpm_ver):
    if ':' in rpm_ver:
        rpm_ver = rpm_ver.split(':', 1)[1]
    rpm_ver = re.split(r'-', rpm_ver)[0]
    return rpm_ver
