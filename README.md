# postman_jsontocsv
A very small Python script to convert a JSON file created using a modified version of sivcan/ResponseToFile-Postman (https://github.com/sivcan/ResponseToFile-Postman) to a CSV.

# Purpose
I could not figure out how to get ResponseToFile-Postman to actually write a CSV so I wrote this script.

# Walkthrough
1. The script takes two arguments, the input JSON file and the output CSV file (include your file extension).
2. Reads in the JSON file written by the modified ResponseToFile-Postman script.
3. Adds brackets, removes newline and comma at end of file and writes a new temp file.
    NOTE: Brackets "[]" are added to make this a JSON array so json.load functions properly
          Newline, comma at EOF are removed to ensure json.load functions properly
4. Writes new CSV with proper newlines and columns

Usage: ./postman_jsontocsv.py [input-file] [outputfile]

# IMPORTANT NOTE
Also included here is the modified ResponseToFile-Postman script.js. Consult the original project for usage.
