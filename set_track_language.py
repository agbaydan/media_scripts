# first run "sudo mkvmerge -J file.mkv" to get track id
# track lists can be 0 based so check if you need to +1 or not if the first one is 0
# then run this with the track id

import os
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(prog="set_track_language", description="set the language of a specific track to english in all mkv files in current directory")
parser.add_argument("track_number", help="The number of the track to set to english. Make sure to use track.properties.number not track.id")
args = parser.parse_args()


trackId = args.track_number
print("Track ID: " + trackId)

directory = os.getcwd()
print("Running in dir: " + directory)

cont = input("Proceed? (y/n): ")

if cont == "n":
    sys.exit()

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print("File: " + f)
        res = subprocess.run(["mkvpropedit", f, "--edit", "track:"+trackId, "--set", "language-ietf=eng", "--set", "name=English"], capture_output=True, text=True)
        if res.returncode == 0:
            print("Successfully ran: " + str(res.args))
            print("Output: \n" + res.stdout)
            print("*********************************************************")
        else:
            print("Error running: " + str(res.args))
            print("Return code: " + res.returncode)
            print(res.stdout)
            print(res.stderr)
            sys.exit()
