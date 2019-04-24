from pathlib import Path
import os

if not os.path.exists("\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData\\v17\\Reports"):
    os.makedirs("\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData\\v17\\Reports")
csvfile = Path("\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData\\v17\\Reports\\services.csv")
servicesCSV = open(csvfile, 'w')