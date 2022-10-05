from time import sleep
from datetime import datetime
# from sh import gphoto2 as gp
import signal, os, subprocess
import gphoto2 as gp


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
# gp(getConfigCommand)


context = gp.Context()
camera = gp.Camera()
camera.init(context)
config_tree = camera.get_config(context)
print('=======')

total_child = config_tree.count_children()
for i in range(total_child):
    child = config_tree.get_child(i)
    text_child = '# ' + child.get_label() + ' ' + child.get_name()
    print(text_child)

    for a in range(child.count_children()):
        grandchild = child.get_child(a)
        text_grandchild = '    * ' + grandchild.get_label() + ' -- ' + grandchild.get_name()
        print(text_grandchild)

        try:
            text_grandchild_value = '        Setted: ' + grandchild.get_value()
            print(text_grandchild_value)
            print('        Possibilities:')
            for k in range(grandchild.count_choices()):
                choice = grandchild.get_choice(k)
                text_choice = '         - ' + choice
                print(text_choice)
        except:
            pass
        print()
    print()

camera.exit(context)