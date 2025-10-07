"""
File: Rig.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from Asset import Asset

class Rig:
    def __init__(self, name):
        self.__name = name
        self.__storage = []              # list of Asset objects
        self.__data_spikes = 2           # starting number of spikes
        self.__removable_drives = 1      # number of drives for extraction
        self.__damage = 0                # how damaged it is
        self.__broken = False            # false = working, true = broken
        self.__upgrade_level = 0         # how many upgrades done
        self.__storage_limit = 3         # how many assets it can hold

    # Add an asset to the rig’s storage
    def add_asset(self, asset):
        if len(self.__storage) >= self.__storage_limit:
            print("Cannot add asset; storage full for rig", self.__name)
            return
        self.__storage.append(asset)

    # Use one data spike for an attack
    def consume_data_spike(self):
        if self.__data_spikes > 0:
            self.__data_spikes = self.__data_spikes - 1
            return True
        return False

    # Take a hit (increase damage)
    def take_hit(self):
        self.__damage = self.__damage + 1
        threshold = 2 + self.__upgrade_level
        if self.__damage >= threshold:
            self.__broken = True

    # Check if rig is broken
    def is_broken(self):
        return self.__broken

    # Use one removable drive for extracting
    def consume_removable_drive(self):
        if self.__removable_drives > 0:
            self.__removable_drives = self.__removable_drives - 1
            return True
        return False

    # Extract only unsecured (unencrypted) assets
    def extract_unsecured_assets(self):
        unsecured = []
        remaining = []
        for a in self.__storage:
            if not a.is_encrypted():
                unsecured.append(a)
            else:
                remaining.append(a)
        self.__storage = remaining
        return unsecured

    # Upgrade rig and increase storage space
    def upgrade(self):
        self.__upgrade_level = self.__upgrade_level + 1
        self.__storage_limit = self.__storage_limit + 2
        print(self.__name, "was upgraded to level", str(self.__upgrade_level))

    # Return rig name
    def get_name(self):
        return self.__name

    # Return internal storage list
    def get_storage(self):
        return self.__storage

    # Return upgrade level
    def get_upgrade_level(self):
        return self.__upgrade_level

    # How it prints
    def __str__(self):
        condition = "Broken" if self.__broken else "Pristine"
        return self.__name + " - " + condition + " (Level " + str(self.__upgrade_level) + ") - Stored: " + str(len(self.__storage))