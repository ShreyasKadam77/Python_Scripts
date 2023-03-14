#                              Duplicate Files Remover with auto scheduled log facility

## script description:
* The objective of this script is to clean directories containing duplicate files and keep a record of those files in a log file.

### How to run script ?
   This script takes 3 command line arguments.
   **`duplicate_file_deleter.py Directory_Name Time_interval Mail_id`**
   where , 
* Directory_Name :- Name of the directory which you want to clean.
* Time_interval :- Script will run periodically after this time interval (in minutes).
* Mail_id :- Email address to which log file will be sent.

#### Note :
          Use -u for usage of script.
          Use -h for help


### How does script works ?

1. Find duplicate files in a directory by comparing hash value of files.
2. Create a log file named as current date time which contains name of duplicate files.
3. Run repeatedly after given interval of time by user.
4. Send created log file to given email id by using user defined email sender module.

