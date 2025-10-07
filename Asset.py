"""
File: Asset.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""



class Asset:
    def __init__(self, name, description):
        # Save basic info
        self.__name = name
        self.__description = description
        # Assets start unencrypted
        self.__encrypted = False

    # Check if encrypted
    def is_encrypted(self):
        return self.__encrypted

    # Encrypt asset (protect it)
    def encrypt(self):
        self.__encrypted = True

    # Decrypt asset (unprotect it)
    def decrypt(self):
        self.__encrypted = False

    # Get asset name
    def get_name(self):
        return self.__name

    # How it prints in text form
    def __str__(self):
        if self.__encrypted:
            return self.__name + ": " + self.__description + " [Encrypted]"
        else:
            return self.__name + ": " + self.__description
