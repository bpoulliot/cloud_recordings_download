#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv, json, sys, os.path, re, requests, zoom_oauth

# Set variables
from_date = "2021-04-06" # dates only need to be 10-digit hyphen-separated
to_date = "2021-04-10"
out_dir = "<out_dir_here"
csv_output = "{}<log_filename_here>.csv".format(out_dir)
page_size = "300" # limit of 300 per Zoom API docs
acct_id = "me" # can be actual ID or 'me' for owner/admin

# get or refresh zoom oauth token
zoom_token = zoom_oauth.get_token()

# Request list of meetings which include download URLs
zoom_uri = "https://api.zoom.us/v2/accounts/{}/recordings".format(acct_id)
params = {
    "page_size": page_size,
    "from": from_date,
    "to" : to_date
    }
headers = {
  "Authorization": "Bearer {}".format(zoom_token)
}

response = requests.get(zoom_uri, headers=headers, params=params).json()
data = response["meetings"]

i = 0
j = 0
rec_count = len(data)
print("{} recordings available, proceeding to download... \n".format(rec_count))
csv_file = open(csv_output, 'w+') #load csv file
output = csv.writer(csv_file) #create a csv.write
output.writerow(data[0].keys())  # header row
while i < rec_count:
    for row in data:
        recording_files = data[i]["recording_files"]
        for file in range(len(recording_files)):
            if recording_files[j]["status"] == "completed":
                file_type = None
                rtype = recording_files[j]["recording_type"]
                file_opt = recording_files[j]["download_url"]
                #print(rtype)
                if rtype == "shared_screen_with_speaker_view" or rtype == "shared_screen_with_speaker_view(CC)":
                    file_type = ".mp4"
                if rtype == "audio_transcript":
                    file_type = ".vtt"
                if rtype == "chat_file":
                    file_type = ".txt"
                if file_type != None:
                    topic = re.sub('[^A-Za-z0-9 ]+',"-",data[i]["topic"])
                    session_dir = "{}{}".format(out_dir,topic)
                    file_down = "{}/{}{}".format(session_dir, topic, file_type)
                    url = "{}?access_token={}".format(file_opt, zoom_token)
                    row[rtype] = "{} downloaded".format(rtype)
                    #print(row["download_{}".format(j)])
                    output.writerow(row.values()) #values row
                    if not os.path.exists(session_dir):
                        os.makedirs(session_dir)
                    #print(file_down)
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
