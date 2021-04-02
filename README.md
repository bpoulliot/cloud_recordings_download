# postman_jsontocsv
A very small Python script to convert a JSON file created using a modified version of sivcan/ResponseToFile-Postman (https://github.com/sivcan/ResponseToFile-Postman) to a CSV.

# Prerequisites
1. Create an OAuth app on the Zoom Marketplace to serve your purposes. Scopes should include creating webinars and meetings. I opted to allow for viewing of these as well.
2. Figure out your OAuth workflow -- using the built-in token retriever in Postman was very useful. If you opt for this route, set the token config to authenticate via browser and ensure the Zoom app's callback URL matches what's in Postman, otherwise the authentication will fail. 
3. Install the ResponseToFile-Postman program. Learn how to run the local server and test it with a few calls, particularly using the appendFile mode and multiple calls at once (i.e, Runner). Examine the JSON files and see that the original program merely pastes the output to the file rather than writing readable JSON.

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
