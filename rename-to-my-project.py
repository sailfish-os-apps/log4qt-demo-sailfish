'''
Created on 23.2.2014

@author: tace (samuli.silvius@gmail.com)
'''

import sys
import os
import argparse
from os import rename

SCRIPT_NAME = os.path.basename(__file__)

def convert_file_names(files, originalName, newName):
    print "\n>>>> Convert file names\n"
    for fname in files:
        if fname.find(originalName) != -1:
            newFullName = fname.replace(originalName, newName, 1)
            rename(fname, newFullName)
            print "Renamed file " + fname + " --> " + newFullName
        else:
            print "File's '" + fname + "' name does not need conversion!"
    print ">>>> DONE converting filenames"
    print "====================================================================\n"

def convert_files_content(files, originalText, newText):
    print "\n>>>> Convert files content\n"
    for file in files:
        newlines = []
        with open(file, 'r') as f:
            found = False
            for i, line in enumerate(f, 1):
                if line.find(originalText) != -1:
                    print "Converting text in file  '" + file + "' at line " + str(i)
                    found = True
                newlines.append(line.replace(originalText, newText))
            if not found:
                print "File " + file + " don't need editing."
        with open(file, 'w') as f:
            for line in newlines:
                f.write(line)
    print ">>>> DONE converting files content"
    print "====================================================================\n"

def get_files(path,
              ignored_dirs=['.git'],
              ignored_files=[SCRIPT_NAME],
              ignore_binary_files=False):
    for prefix, dirs, files in os.walk(path):
        for ignore in ignored_dirs:
            if ignore in dirs:
                dirs.remove(ignore)
                print "Ignored dir: " + ignore
        for name in files:
            ignored = False
            for ignore in ignored_files:
                if ignore in name:
                    files.remove(ignore)
                    ignored = True
                    print "Ignored file: " + ignore
            if not ignored:
                filename = os.path.join(prefix, name)
                if ignore_binary_files and is_binary(filename):
                    print filename + " is BINARY file and ignored by default!"
                else:
                    yield filename

def is_binary(filename):
    """
    Return true if the given filename appears to be binary.
    File is considered to be binary if it contains a NULL byte.
    FIXME: This approach incorrectly reports UTF-16 as binary.
    """
    with open(filename, 'rb') as f:
        for block in f:
            if '\0' in block:
                return True
    return False

def check_args(args):
    if not args.newName.startswith('harbour-'):
         print "Your new app name MUST start with \"harbour-\""
         sys.exit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('newName', help='New name of your program')
    parser.add_argument('--originalName', nargs='?', default='harbour-helloworld-pro-sailfish', help="Default is '%(default)s'")
    parser.add_argument('--ignoredDirs', nargs='*', default=['.git'], help="Give a list of dir paths separated with space. Default is '%(default)s'")
    parser.add_argument('--ignoredFiles', nargs='*', default=[SCRIPT_NAME], help="Give a list of file paths separated with space. Default is '%(default)s'")
    args = parser.parse_args()
    check_args(args)

    files = get_files(".", args.ignoredDirs, args.ignoredFiles)
    convert_file_names(files, args.originalName, args.newName)
    files = get_files(".", args.ignoredDirs, args.ignoredFiles, ignore_binary_files=True)
    convert_files_content(files, args.originalName, args.newName)


if __name__ == '__main__':
    main()
