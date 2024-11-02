import os
import argparse
from winreg import *

def sid2user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE,
                      r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
                      + '\\' + sid)
        value, _ = QueryValueEx(key, 'ProfileImagePath')
        user = value.split('\\')[-1]
        return user
    except Exception as e:
        return sid

def returnDir():
    dirs = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
    for recycleDir in dirs:
        if os.path.isdir(recycleDir):
            return recycleDir
    return None

def findRecycled(recycleDir):
    if recycleDir is None:
        print("[!] No Recycle Bin directory found.")
        return
    dirList = os.listdir(recycleDir)
    for sid in dirList:
        user = sid2user(sid)
        userDir = os.path.join(recycleDir, sid)
        if os.path.isdir(userDir):
            try:
                files = os.listdir(userDir)
                print('\n[*] Listing Files For User: ' + str(user))
                for file in files:
                    print('[+] Found File: ' + str(file))
            except PermissionError:
                print(f"[!] Permission denied for directory: {userDir}")

def main():
    parser = argparse.ArgumentParser(description="Recycle Bin Analyzer")
    args = parser.parse_args()
    recycledDir = returnDir()
    findRecycled(recycledDir)

if __name__ == '__main__':
    main()
