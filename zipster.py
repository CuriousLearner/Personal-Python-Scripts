#! /usr/bin/python3

import os
import sys
import zipfile
import zlib
import argparse

parser = argparse.ArgumentParser(description = "Zip File Creator.")

parser.add_argument('-z','--zipname', 
                    dest = "zipname", 
                    action = 'store', 
                    help = 'Takes the Zip Package name.')
parser.add_argument('-f','--force', 
                     dest = "force", 
                     action = 'store_true', 
                     default = False,
                     help = 'Force to replace the zip package, if it already exists')
parser.add_argument('--files', 
                     nargs = '*', 
                     action = 'store', 
                     help = 'Takes the full path of the files to be zipped.')
parser.add_argument('-v','--view', 
                     dest = 'view', 
                     action = 'store_true', 
                     default = False, 
                     help = 'View the details of files before and after compression.')

args = parser.parse_args()

def zipit(zipname, path, mode):
    with zipfile.ZipFile(zipname, mode) as zp:
        for each_path in path:
            filename = os.path.basename(each_path)
            newpath = os.path.dirname(each_path)
            current_dir = os.getcwd()
            os.chdir(newpath)
            zp.write(filename, compress_type = zipfile.ZIP_DEFLATED)
            print("File " + str(filename) + " is added to the archive.")
            os.chdir(current_dir)

def view_details(archive_name):
    print('Now displaying the details of the file before and after compression.')
    archive = zipfile.ZipFile(archive_name)
    for info in archive.infolist():
        print(info.filename)
        print('\t\tUncompressed Size: \t' + str(info.file_size) + ' bytes')
        print('\t\tCompressed Size: \t' + str(info.compress_size) + ' bytes')

if __name__ == '__main__':
   
    if args.force:
        zipit(args.zipname, args.files, "w")
        print("All files are added to the archive.")
        if args.view:
            view_details(args.zipname)
        sys.exit(0)

    if args.zipname in os.listdir(os.curdir):
        choice = input("The Zip Package already exists. Do you want to replace it? (y/n) ")
        if choice == 'y':
            zipit(args.zipname, args.files, "w")
            print("All files are added to the archive.")
            if args.view:
                view_details(args.zipname)
            sys.exit(0)
        elif choice == 'n':
            print("Zip Package not replaced. Try to zip again. Exiting!")
            sys.exit(1)

        else:
            print("Wrong Choice, try again. Exiting")
            sys.exit(1)
    else:
        zipit(args.zipname, args.files, "w")
        print("All files are added to the archive.")
        if args.view:
            view_details(args.zipname)

