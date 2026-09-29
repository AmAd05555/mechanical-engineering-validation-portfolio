import json
from pathlib import Path
from parametric_motor_mount import DEFAULT, deterministic_checks
print(json.dumps(deterministic_checks(DEFAULT), indent=2))
