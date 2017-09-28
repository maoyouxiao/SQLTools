#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import json
import sqlite3
from datetime import datetime

try:
    import urlparse as parse
except ImportError:
    from urllib import parse

def printDownloads(dbname):
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute("select * from moz_anno_attributes where name like 'downloads%';")
        for id, name in c:
            if 'fileuri' in name.lower():
                file_id = id
            if 'metadata' in name.lower():
                data_id = id
        c.execute("select place_id, content from moz_annos where anno_attribute_id=?;", [file_id])
        destfiles = c.fetchall()
        print("\n[*] --- Files Downloaded ---")
        for place_id, content in destfiles:
            attrs = {}.fromkeys(['path', 'date', 'url'])
            attrs['path'] = parse.unquote(parse.urlsplit(content).path)
            c.execute("select content from moz_annos where anno_attribute_id=? and place_id=?;", [data_id, place_id])
            attrs['date'] = datetime.fromtimestamp(json.loads(c.fetchone()[0])['endTime'] / 1000).strftime("%y-%m-%d %H:%M:%S")
            c.execute("select url from moz_places where id=?;", [place_id])
            attrs['url'] = c.fetchone()[0]
            print("[+] File: %s from source: %s at: %s" % (attrs['path'], attrs['url'], attrs['date']))
        c.close()
        conn.close()
    except Exception as e:
        if 'encrypted' in str(e):
            print("\n[*] Error reading your cookies database.")
            print("[*] Upgrade your Python-Sqlite3 Library.")
            sys.exit(1)

def printCookies(dbname):
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute("SELECT host, name, value FROM moz_cookies;")
        print("\n[*] -- Found Cookies --")
        for host, name, value in c:
            print("[+] Host: %s, Cookie: %s, Value: %s" % (host, name, value))
        c.close()
        conn.close()
    except Exception as e:
        if 'encrypted' in str(e):
            print("\n[*] Error reading your cookies database.")
            print("[*] Upgrade your Python-Sqlite3 Library.")
            sys.exit(1)

def printHistory(dbname):
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute("select url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits where visit_count > 0 and moz_places.id == moz_historyvisits.place_id;")
        print("\n[*] -- Found History --")
        for row in c:
            print("[+] %s - Visited: %s" % row)
        c.close()
        conn.close()
    except Exception as e:
        if 'encrypted' in str(e):
            print("\n[*] Error reading your cookies database.")
            print("[*] Upgrade your Python-Sqlite3 Library.")
            sys.exit(1)

def printGoogle(dbname):
    try:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute("select url, datetime(visit_date/1000000, 'unixepoch') from moz_places, moz_historyvisits where visit_count > 0 and moz_places.id == moz_historyvisits.place_id;")
        print("\n[*] -- Found Google --")
        for url, date in c:
            if 'google' in url.lower():
                r = re.findall(r'q=.*\&?', url)[0]
                if r:
                    search = parse.unquote_plus(r.split("&")[0][2:])
                    print("[+] %s - Searched For: %s" % (date, search))
        c.close()
        conn.close()
    except Exception as e:
        if 'encrypted' in str(e):
            print("\n[*] Error reading your cookies database.")
            print("[*] Upgrade your Python-Sqlite3 Library.")
            sys.exit(1)

def main():
    if not sys.argv[1:]:
        print("Usage: %s <firefox profile path>" % sys.argv[0])
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.isdir(path):
        print("[!] Path Does Not Exist: %s" % path)
        sys.exit(1)
    else:
        dbname = os.path.join(path, "cookies.sqlite")
        if os.path.isfile(dbname):
            printCookies(dbname)
        else:
            print("[!] Cookies DB does not exist: %s" % dbname)
        dbname = os.path.join(path, "places.sqlite")
        if os.path.isfile(dbname):
            printHistory(dbname)
            printDownloads(dbname)
            printGoogle(dbname)
        else:
            print("[!] Places DB does not exist: %s" % dbname)

if __name__ == "__main__":
    main()
