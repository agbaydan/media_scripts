# first run "sudo mkvmerge -J file.mkv" to get track number
# use track.properties.number not track.id
# then run this with the track id

import os
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(prog="set_default_track", description="program that will set default track in a directory of mkv files")
parser.add_argument("track_numbers", help="A comma separated list of track numbers to edit. They will all get set to default=false")
parser.add_argument("default_track", help="A track number that will set default=true on. Make sure to use track.properties.number not track.id")
parser.add_argument("-e", "--exit-on-error", help="Bool value indicating if script should cancel if an error occurs. Defaults to true if absent", choices=["true","false","t","f"], default="true", required=False)
args = parser.parse_args()

ids = args.track_numbers.split(",")
print("Track IDS: " + str(ids))

defId = args.default_track
print("Track to default: " + defId)

exitOnError = True
if args.exit_on_error == "false" or args.exit_on_error == "f":
    exitOnError = False

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
        for trackId in ids:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Track id " + trackId + "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            res = ""
            if trackId == defId:
                res = subprocess.run(["mkvpropedit", f, "--edit", "track:"+trackId, "--set", "flag-default=true"], capture_output=True, text=True)
            else:
                res = subprocess.run(["mkvpropedit", f, "--edit", "track:"+trackId, "--set", "flag-default=false"], capture_output=True, text=True)
            if res.returncode == 0:
                print("Successfully ran: " + str(res.args))
                print("Output: \n" + res.stdout)
                print("*********************************************************")
            else:
                print("Error running: " + str(res.args))
                print("Return code: " + str(res.returncode))
                print(res.stdout)
                print(res.stderr)
                if exitOnError:
                    sys.exit()
