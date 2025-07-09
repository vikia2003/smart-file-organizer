# smart-file-organizer

Built by Viktorija Angelovska

A simple and user-friendly Python application that automatically organizes files in a chosen folder into subfolders based on their file extensions. Includes an undo feature, logging, and a graphical interface built with Tkinter.

FEATURES
Scans a selected folder for files
Classifies files by extension (e.g., .jpg, .pdf, .txt)
Creates corresponding subfolders and moves files accordingly
Maintains a log (file_log.json) of moved files with timestamps
Undo last organize operation functionality
Intuitive GUI with folder selection, organize, and undo buttons
Handles filename conflicts by renaming files to avoid overwriting
Basic error handling for permissions and file access issues
USAGE
RUNNING THE APPLICATION
In order to run the application, just run the python script ‘python organizer.py’.
ORGANIZING FILES
Click the ‘Pick a folder to organize’ button. Select the folder containing files to organize. The program will classify and move files into extension-based subfolders automatically.
[see screenshot named 'organizer_1']
Select the folder containing files to organize. The program will classify and move files into extension-based subfolders automatically.
[see screenshot named 'organizer_2']
On success, a popup confirms completion.
[see screenshot named 'organizer_3']
UNDO LAST OPERATION
Click ‘Undo last operation’ to revert the most recent organizing action.
[see screenshot named 'organizer_4']
A popup will notify you whether the undo was successful or if errors occurred.
[see screenshot named 'organizer_5']
LOGGING
All file move operations are logged in file_log.json inside the selected folder. Each batch includes source, destination, and timestamp info for possible undo operations.

KNOWN LIMITATIONS
Undo only works for the last operation logged. There is also no support for nested folder organizing yet, and permission issues may prevent file moves on restricted folders.
