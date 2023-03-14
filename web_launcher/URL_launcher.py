from sys import *
from urllib.request import urlopen
import webbrowser
import re

def is_connected():
    """
    This function checks if internet is connected or not by simply opening google.com
    :return: True if internet is connected else False
    """
    try:
        result = urlopen("https://www.google.com")
        return True
    except Exception as err:
        return False

def find_link(line):
    """
    This function finds only URLs in a line by using regular expression.
    :param line: line of any file
    :return: url founded
    """
    url = re.findall("^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$", line)
    return url

def web_launch(link_file_path):
    """
    This function open URLs in new tabs of a browser.
    :param link_file_path: path of file which contains URLs to be opened.
    """
    with open(link_file_path) as fp:
        for line in fp:
            urls = find_link(line)
            for link in urls:
                webbrowser.open(link, new = 2)

def main():
    print("------------- Automation Script -------------")
    print(f"Automation script started with name : {argv[0]}.")


    if ((argv[1] == "-h") or (argv[1] == "-H")):
        print("Help : This script is used to open URL links in text file in different tabs.")
        exit()

    if ((argv[1] == "-u") or (argv[1] == "-U")):
        print("Usage : Application Name File_path_containing_links")
        exit()

    if (len(argv) != 2):
        print("Error : Insufficient Arguments.")
        print("Use -h for help and Use -u for usage of the script.")
        exit()


    try:
        if is_connected():
            web_launch((argv[1]))
        else:
            print("Unable to connect to internet...")

    except ValueError:
            print("Error : Invalid datatype of input")

    except Exception as E:
            print(f"Error : {E}")


if __name__ == "__main__":
    main()