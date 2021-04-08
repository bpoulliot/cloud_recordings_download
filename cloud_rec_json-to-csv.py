#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv, json, sys
#if you are not using utf-8 files, remove the next line
#check if you pass the input file and output file
if sys.argv[1] is not None and sys.argv[2] is not None:
    fileInput = sys.argv[1]
    fileOutput = sys.argv[2]
    inputFile = open(fileInput) #open json file
    outputFile = open(fileOutput, 'w') #load csv file
    rdata = json.load(inputFile) #load json content
    inputFile.close() #close the input file
    data = rdata["meetings"]
    i = 0
    j = 0
    print(len(data))
    output = csv.writer(outputFile) #create a csv.write
    output.writerow(data[0].keys())  # header row
    while i < len(data):
        for row in data:
            recording_files = data[i]["recording_files"]
            for file in range(len(recording_files)):
                if recording_files[j]["status"] == "completed":
                    rtype = recording_files[j]["recording_type"]
                    print(rtype)
                    if rtype == "shared_screen_with_speaker_view" or rtype == "shared_screen_with_speaker_view(CC)":
                        row["download_{}".format(j)] = recording_files[j]["download_url"]
                        print(row["download_{}".format(j)])
                        output.writerow(row.values()) #values row
                    j += 1
            i += 1
            j = 0
