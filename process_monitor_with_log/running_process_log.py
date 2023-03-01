import psutil
import os
import time
from sys import *

import schedule


def Process_Display(log_dir = "marvellous"):
    list_process = []

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    seperator = "-" * 80
    log_path = os.path.join(log_dir, "running_processes_log%s.log"%(time.time()))
    f = open(log_path, 'w')
    f.write(seperator + "\n")
    f.write(f"Marvellous Infosystems Process Logger : {time.ctime()} \n")
    f.write(seperator + "\n")

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            # vms = proc.memory_info().vms/(1024 * 1024)
            # pinfo['vms'] = vms
            list_process.append(pinfo)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    for element in list_process:
        f.write("%s\n" % element)

def main():
    print("------------- Marvellous Infosystems Automations -------------")
    print(f"Automation script started with name : {argv[0]}.")

    if ((argv[1] == "-h") or (argv[1] == "-H")):
        print("Help : This script is used to display all running processes.")
        exit()

    if ((argv[1] == "-u") or (argv[1] == "-U")):
        print("Usage : Application Name AbsolutePath_of_Directory")
        exit()

    if (len(argv) != 2):
        print("Error : Insufficient Arguments.")
        print("Use -h for help and Use -u for usage of the script.")
        exit()

    try:
        # schedule.every(int(argv[1]).minutes.do.Process_Display(argv[1]))
        Process_Display(argv[1])
    except ValueError:
        print("Error : Invalid datatype of input")

    except Exception:
        print("Error : Invalid input")

if __name__ == "__main__":
    main()