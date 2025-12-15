from pathlib import Path

# PATH CONSTANTS
DATA_URL = "https://archive.ics.uci.edu/static/public/447/condition+monitoring+of+hydraulic+systems.zip"

DATA_CACHE_PATH = Path("data_cache")
DATA_HYDROLIC_PATH = DATA_CACHE_PATH / Path("hydraulic_ics")

PS2_PATH = DATA_HYDROLIC_PATH / Path("PS2.txt")
FS1_PATH = DATA_HYDROLIC_PATH / Path("FS1.txt")
PROFILE_PATH = DATA_HYDROLIC_PATH / Path("profile.txt")

# OTHER CONSTANTS

TRAINING_LIMIT = 2_000
