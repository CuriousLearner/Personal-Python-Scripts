#! /usr/bin/python3

import argparse
import requests

parser = argparse.ArgumentParser(description = 'Check URL')

parser.add_argument('--file',
                    dest = 'filename',
                    action = 'store',
                    nargs = 1,
                    help = 'Take file to read urls.')

args = parser.parse_args()

if args.filename:
    for files in args.filename:
        with open(files,'r') as urlfile:
            try:
                for url in urlfile:
                    url = url.rsplit()[0]
                    req = requests.get(url)
                    if req.status_code == 200:
                        print("Working: " + url)
                    else:
                        print("Url " + url + " does not exist.")
            except requests.exceptions.ConnectionError:
                print("Connection Error")
            except requests.exceptions.MissingSchema:
                print("Missing Schema")
            finally:
                urlfile.close()
