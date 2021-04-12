#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### Purpose: Download account recordings from a main account in zoom and log to
###          CSV file what files are downloaded -- skips previously downloaded.
### Limitations:
###             * Account must be administrator or owner
###             * Only 300 recordings at a time (pagination not built in)
###             * CSV currently overwrites each time (for testing purposes)
###             * Uses requests (non-standard library)
###             * No error handling, tracebacks not descriptive enough
###             * Need better URL building
###             * Does not provide for OAuth workflow (in progress)
###
### Usage: ./download_account_recordings.py
### NOTE: Easily modified for variable output directories, test for sys.argv
###
### Process: 1. GET list of cloud recordings in account (300 max at the moment)
###          2. Find available recording files (supported: MP4, TXT, VTT)
###          3. Create dirs for each session name w/ only alphanumeric chars
###          4. Log each file downloaded + complete API response to CSV
###          5. Download each file w/ only alphanumeric chars in filename

# NOTE: Import of "creds" is credentials file, not a Python library
import csv, json, sys, creds, os.path, re, requests

# Set variables
from_date = "2021-04-06" # dates only need to be 10-digit hyphen-separated
to_date = "2021-04-10"
out_dir = "<your_out_dir_here>"
csv_output = "{}<your_log_file_here>.csv".format(out_dir)
page_size = "300" # limit of 300 per Zoom API docs
acct_id = "me" # can be actual ID or 'me' for owner/admin

# Request list of meetings which include download URLs
zoom_uri = "https://api.zoom.us/v2/accounts/{}/recordings".format(acct_id)
params = {
    "page_size": page_size,
    "from": from_date ,
    "to" : to_date
    }
headers = {
  "Authorization": "Bearer {}".format(creds.zoom_token)
}

response = requests.get(zoom_uri, headers=headers, params=params).json()
data = response["meetings"]

i = 0 # index for each meeting available
j = 0 # index for each recording file (MP4, TXT chat, VTT transcript)
rec_count = len(data)
print("{} recordings available, proceeding to download...\n".format(rec_count))
csv_file = open(csv_output, 'w+') #load csv file
output = csv.writer(csv_file) #create a csv.write
output.writerow(data[0].keys())  # header row
while i < rec_count:
    for row in data:
        recording_files = data[i]["recording_files"]
        for file in range(len(recording_files)):
            # only download recording files that are complete
            if recording_files[j]["status"] == "completed":
                # set to None for later test
                file_type = None
                rtype = recording_files[j]["recording_type"]
                file_opt = recording_files[j]["download_url"]
                # set file extension for each recording file
                if rtype == "shared_screen_with_speaker_view" or \
                   rtype == "shared_screen_with_speaker_view(CC)":
                    file_type = ".mp4"
                if rtype == "audio_transcript":
                    file_type = ".vtt"
                if rtype == "chat_file":
                    file_type = ".txt"
                # if recording files exist, download them
                if file_type != None:
                    # get rid of non-alphanumeric characters
                    topic = re.sub('[^A-Za-z0-9 ]+',"-",data[i]["topic"])
                    session_dir = "{}{}".format(out_dir,topic)
                    file_down = "{}/{}{}".format(session_dir, topic, file_type)
                    url = "{}?access_token={}".format(file_opt, creds.zoom_token)
                    row[rtype] = "{} downloaded".format(rtype) # add files DL'd
                    # write row to CSV
                    output.writerow(row.values()) #values row
                    if not os.path.exists(session_dir):
                        os.makedirs(session_dir)
                    # check if file already exists
                    if not os.path.isfile(file_down):
                        print("Downloading file: {}\n".format(file_down))
                        r_file = requests.get(url, allow_redirects=True)
                        open(file_down, 'wb').write(r_file.content)
                    else:
                        print("File {} exists, moving on...\n".format(file_down))
                j += 1
        i += 1
        j = 0
print("Cloud Recordings download complete.")
