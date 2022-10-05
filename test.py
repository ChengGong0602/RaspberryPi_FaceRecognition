from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess


clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "--delete-all-files", "-R"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]
getConfigCommand = ["--auto-detect","--list-config"]

# folder_name = shot_date + picID
# save_location = "/home/pi/Desktop/gphoto/images/" + folder_name



def killGphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    # Search for the process we want to kill
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            # Kill that process!
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

# def get_configuration():



killGphoto2Process()
gp(getConfigCommand)