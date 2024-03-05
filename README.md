# Huawei Sports Watch track data to .gpx conversion

## Description

Huawei Sport watches don't allow users to directly export workout track data from workout records to .gpx files. This Python script remedies that.

## How to

- You need to have Python 3.7+ installed
- You need to acquire your Huawei Health data, either from your backups, which may be tricky, or by requesting the data from Huawei. The latter may take days.
- After you have the data, copy your `"HUAWEI_HEALTH_YYYYMMDDHHMMSS\Motion path detail data & description\motion path detail data.json"` in same directory with hi2gpx.py or vice versa.
- Run the script: `python hi2gpx.py`

Assuming your Python is installed and set up correctly, the script should extract all the track data from `motion path detail data.json` in separate .gpx files, of which there may be many. E.g. in my case the number of extracted workouts was 277.  

The filenames will look something like `20230329_205030-20230329_211943-sport_type_4.gpx`. The filenames contain the start time of the workouts in the local time of the computer the extraction was run on, then the end time of the workouts, then the number of the sport types. I used the number of the sport types instead of name of the sports, because it seemed different numbers might correspond to different sport types on different devices.

## Might add later on...

- Argument parsing
  - passing source filename and destination directory as parameters
  - additional extraction format (.gpx/.tcx)
  - chance to freely select time zone
- Activity/sport types as strings instead of numbers
- GUI (tkinter)
- Web service to do the conversion for those who can't or don't want to bother dealing with the code themselves and just want to extract .gpx files from their data
