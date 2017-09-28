#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3

def printProfile(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT fullname, skypename, emails, phone_home, phone_mobile, city, country, datetime(profile_timestamp, 'unixepoch') FROM Accounts")
    for row in c:
        print("[*] -- Found Account --")
        print("[+] User: %s" % row[0])
        print("[+] Skype Username: %s" % row[1])
        print("[+] Emails: %s" % row[2])
        print("[+] Telephone: %s" % row[3])
        print("[+] Mobile: %s" % row[4])
        print("[+] Location: %s,%s" % (row[5], row[6]))
        print("[+] Profile Date: %s" % row[7])
    c.close()
    conn.close()

def printContacts(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT displayname, skypename, city, country, phone_mobile, birthday FROM Contacts;")
    for row in c:
        print("\n[*] -- Found Contact --")
        print("[+] User: %s" % row[0])
        print("[+] Skype Username: %s" % row[1])
        if row[2] or row[3]:
            print("[+] Location: %s,%s" % (row[2], row[3]))
        if row[4]:
            print("[+] Mobile: %s" % row[4])
        if row[5]:
            print("[+] Birthday: %s" % row[5]) 
    c.close()
    conn.close()

def printCallLog(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    # c.execute("SELECT datetime(begin_timestamp, 'unixepoch'), identity FROM calls, conversations WHERE calls.conv_dbid = conversations.id;")
    c.execute("SELECT datetime(creation_timestamp, 'unixepoch'), identity FROM conversations;")
    print("\n[*] -- Found Calls --")
    for row in c:
        print("[+] Time: %s | Partner: %s" % row)
    c.close()
    conn.close()

def printMessages(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute("SELECT datetime(timestamp, 'unixepoch'), chatname, author, body_xml FROM Messages;")
    print("\n[*] -- Found Messages --")
    for row in c:
        try:
            if "partlist" not in str(row[3]):
                if not row[1] == row[2]:
                    msgDirection = "To %s: " % row[1]
                else:
                    msgDirection = "From %s: " % row[2]
                print("Time: %s %s %s" % (row[0], msgDirection, row[3]))
        except Exception:
            pass

def main():
    if not sys.argv[1:]:
        print("Usage: %s <skype profile path>" % sys.argv[0])
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.isdir(path):
        print("[!] Path Does Not Exist: %s" % path)
        sys.exit(1)
    else:
        skypeDB = os.path.join(path, "main.db")
        if os.path.isfile(skypeDB):
            printProfile(skypeDB)
            printContacts(skypeDB)
            printCallLog(skypeDB)
            printMessages(skypeDB)
        else:
            print("[!] Skype Database does not exist: %s" % skypeDB)

if __name__ == "__main__":
    main()





