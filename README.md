HandBrake Batch MultiCut

Tool with GUI to batch split / cut files and convert with Handbrake CLI

IMPORTANT: Download HandBrakeCLI.exe from official Website and put in your Handbrake install directory (C:\Program Files\HandBrake)

How it works:
- From HANDBRAKE
    1) Open a only one file
    2) Apply your presets (including or not the chapter or time range to cut)
    3) "Enqueue"
    4) From "Queue" go to "Options"
    5) "Export the queue (CLI Only)"

- From HANDBRAKE MANAGER
    1) Open the exported JSON File
    2) Select the source source folder where you have all the files to split /cut
    3) Select your destination folder
    4) Options : 
          - Check "Change ranges" and add new ranges to cut your video files in muliples parts
          - Uncheck the files that will not be cutted and converted
    5) Click on "Generate JSON file and Preview" to check the new JSON file
    6) Click on "Launch HandBrakeCLI"


