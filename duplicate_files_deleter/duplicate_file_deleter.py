import datetime
import os
from sys import *
import hashlib
import time
import schedule
from email_sender import send_mail


def hashfile(path, blocksize=1024):
    """
     function uses md5 hashing algorithm to get hash value of file in hexadecimal digits.
        It takes two parameters as:
    :param path: path of file whose hash value is to be returned.
    :param blocksize: reads only given bytes from file.

    :return: hexadecimal digit value for given file.

    """

    afile = open(path, 'rb')
    hasher = hashlib.md5()

    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()

    return hasher.hexdigest()


def find_duplicates(dir_name):
    """
     function returns dictionary containing all the identical files with same key (checksum of file).
        It takes one parameter as:
    :param dir_name: directory name from which we need to find duplicate files.

    """

    flag = os.path.isabs(dir_name)
    if flag == False:
        dir_name = os.path.abspath(dir_name)

    exists = os.path.isdir(dir_name)

    dups = {}

    if exists:
        for foldername, subfolder, filenames in os.walk(dir_name):
            for fnames in filenames:
                path = os.path.join(foldername, fnames)
                filehash = hashfile(path)
                if filehash in dups:
                    dups[filehash].append(path)
                else:
                    dups[filehash] = [path]
        return dups
    else:
        print("Invalid Path")


def create_log_of_duplicates(dict1, log_dir="Duplicates"):
    """
     function creates log file containing names of all duplicate files.
        It takes two parameters as :
    :param dict1: dictionary containing checksum and it's files as key-values pair.
    :param log_dir: directory name in which log files are going to create.

    :return: path of created log file.
    """
    results = list(filter(lambda x: len(x) > 1, dict1.values()))

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass
    log_path = os.path.join(log_dir, "%s.log" % datetime.datetime.now().strftime("%d-%m-%Y, %H-%M-%S"))
    f = open(log_path, 'w')

    if len(results) > 0:
        # f.write("Duplicates Found: ")
        f.write("The following files are duplicates." + "\n")

        icnt = 0
        for result in results:
            for subresult in result:
                icnt += 1
                if icnt >= 2:
                    # print(subresult)
                    f.write(subresult + "\n")
            icnt = 0
        return log_path
    else:
        f.write("No duplicates are found.")

def delete_duplicates(dict1):
    """
    function deletes all the duplicate files found from the dictionary.
        It takes one parameter as :
    :param dict1: dictionary containing checksum and it's files as key-values pair.

    :return: 'n' total number of duplicate files which are deleted.

    """
    results = list(filter(lambda x: len(x) > 1, dict1.values()))

    if len(results) > 0:
        n = 0
        icnt = 0
        for result in results:
            for subresult in result:
                icnt += 1
                if icnt >= 2:
                    n += 1
                    os.remove(subresult)
            icnt = 0
        return n

    else:
        pass


def main():
    print(" *****************  Automation Script *****************")
    print("")

    if (argv[1] == "-h"):
        print("This script will delete duplicate files from directory and create a log of deleted filenames, repeat "
              "this task after given time interval and send that log file to given mail id .")
        exit()

    if (argv[1] == "-u"):
        print("Usage : script_name Directory_name Time_interval Mail_id")
        exit()

    if len(argv) != 4:
            print("Insufficient Arguments")
            exit()

    def run():
        try:
            arr = {}
            ScanstartTime = datetime.datetime.now()
            arr = find_duplicates(argv[1])
            # total_files_scanned = len(arr.values())
            file = create_log_of_duplicates(arr)

            num = delete_duplicates(arr)
            send_mail(file, argv[3], ScanstartTime, num)
            # endTime = time.time()
            print("Script is running...")

        except Exception as E:
            # print(f'Error : Invalid input {E}')
            pass

    schedule.every(int(argv[2])).minutes.do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()