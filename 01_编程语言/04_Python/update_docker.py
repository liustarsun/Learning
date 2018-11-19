#!/usr/local/bin/python3
import os
import subprocess


def operate_dockers(name, list_command, delete_command):
    # list command
    print("List " + name + "....")
    [status, result] = subprocess.getstatusoutput(list_command)

    if result:
        # delete command
        delete_command = delete_command + result
        print("Start delete the " + name + ": " + delete_command)
        [status, result] = subprocess.getstatusoutput(delete_command)

        # False, 0
        if not status:
            print("Delete " + name + " finished!!")
            return "Successed"
        else:
            print("Delete " + name + " failed, Exit!!")
            quit()
    else:
        print("There is no " + name + "!")
        return "Successed"
        pass


# delete containers
name = "containers"
list_containers_cmd = "echo $(docker ps -aq)"
delete_containers_cmd = "docker rm "
result = operate_dockers(name, list_containers_cmd, delete_containers_cmd)

# delete images
if result == "Successed":
    name = "images"
    list_images_cmd = "echo $(docker image list -aq)"
    delete_images_cmd = "docker rmi -f "
    operate_dockers(name, list_images_cmd, delete_images_cmd)
else:
    pass
