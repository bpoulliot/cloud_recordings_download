# postman_jsontocsv
A very small Python script to convert a JSON file created using a modified version of sivcan/ResponseToFile-Postman (https://github.com/sivcan/ResponseToFile-Postman) to a CSV.

# Prerequisites
1. Create an OAuth app on the Zoom Marketplace to serve your purposes. Scopes should include creating webinars and meetings. I opted to allow for viewing of these as well.
2. Figure out your OAuth workflow -- using the built-in token retriever in Postman was very useful. If you opt for this route, set the token config to authenticate via browser and ensure the Zoom app's callback URL matches what's in Postman, otherwise the authentication will fail. 
3. Install the ResponseToFile-Postman program. Learn how to run the local server and test it with a few calls, particularly using the appendFile mode and multiple calls at once (i.e, Runner). Examine the JSON files and see that the original program merely pastes the output to the file rather than writing readable JSON.

# Purpose
I could not figure out how to get ResponseToFile-Postman to actually write a CSV so I wrote this script.

# Scripts

## postman_jsontocsv.py
1. The script takes two arguments, the input JSON file and the output CSV file (include your file extension).
2. Reads in the JSON file written by the modified ResponseToFile-Postman script.
3. Adds brackets, removes newline and comma at end of file and writes a new temp file.
    NOTE: Brackets "[]" are added to make this a JSON array so json.load functions properly
          Newline, comma at EOF are removed to ensure json.load functions properly
4. Writes new CSV with proper newlines and columns

Usage: ./postman_jsontocsv.py [input-file] [outputfile]

## cloud_rec_json-to-csv.py
1. Two arguments, input JSON from Postman that returns cloud recordings and destination file.
2. SEE postman_jsontoCSV.py walkthrough

Usage: ./cloud_rec_json-to-csv.py [input-file] [outputfile]

## zoom_oauth.py
NOTE: Depends on rauth Python library (may be unmaintained -- will search for better alternative)

A Python script, defines a function that either fetches a token or refreshes an existing token. Not terribly secure, use at your own risk.

1. Checks for existing refresh token in JSON credentials file
2. If present: 
    a. Sends a request to Zoom API to renew token authorization
    b. Writes refresh token to JSON creds file from API response
    c. Returns Zoom OAuth2 token
4. If not present:
    a. Sends request for authorization to Zoom
    b. Opens web browser to Zoom + redirect URL
    c. Requests user input of redirect URL (includes authorization code for token request)
    d. Sends a request for an OAuth2 token using authorization code from #4c
    e. Writes refresh token to JSON creds file from API response
    f. Returns Zoom OAuth2 token
    
Usage: N/A (used in download_account_recordings) -- can be used on its own if needed

## download_account_recordings.py
NOTE: Dependency on zoom_oauth.py. Requires some configuration such as output dir, dates, CSV log file name, Zoom account ID (if not using "me")...

1. Uses zoom_oauth.py to get an Oauth2 token or refresh an existing token.
2. Grabs a list of cloud recordings from an account -- CURRENTLY ACCOUNT LEVEL ONLY, MAX 300 RECORDINGS
3. Documents the JSON response for each recording in a CSV
4. Downloads 3 files (if present, must be "completed" status): MP4 recording, TXT chat file, VTT audio transcript
5. Renames files (using "topic" from API response) to alphanumeric, replaces illegal characters with hyphens (regular expression can be customized)
6. Creates folders for each recording (using "topic" from API response) w/ same replacement scheme as #5

Usage: ./download_account_recordings.py

# Postman Collection for Zoom
Here's the collection I used:
https://marketplace.zoom.us/docs/guides/guides/postman/using-postman-to-test-zoom-apis

users > {user Id} > meetings > [POST] Create a Meeting
users > {user Id} > webinars > [POST] Create a Webinar (requires some modification of sample CSV)
meetings > [GET] Get a Meeting (need 10-digit numeric meeting ID)
webinars > [GET] Get a Webinar (used to get Start URL for webinars)

# Meeting Settings
I sent meeting settings as raw JSON, as that's the only way I could get it to work. Check the meeting_settings.json file.

# IMPORTANT NOTE
Also included here is the modified ResponseToFile-Postman script.js. Consult the original project for usage.

I've included a sample CSV for use with the Create a Meeting Endpoint.
