"""
File: Rig.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
# Rig.py
# Represents a rig (computer). It can take hits, be upgraded, repaired, and hold assets.

from Asset import Asset, check_asset

class Rig:
    def __init__(self, name):
        self.__name = name
        self.__storage = []

        # default resources — all rigs start with these strings
        self.__storage.append("Data Spike")
        self.__storage.append("Data Spike")
        self.__storage.append("Removable Drive")

        # damage and condition tracking
        self.__damage = 0
        self.__broken = False

        # level affects toughness and storage
        self.__upgrade_level = 0
        self.__storage_limit = 5

    # Add an asset or resource if there’s room
    def add_asset(self, asset):
        if len(self.__storage) >= self.__storage_limit:
            print("Cannot add asset; storage full for rig", self.__name)
            return
        self.__storage.append(asset)

    # Remove a Data Spike (used in attacks)
    def consume_data_spike(self):
        if "Data Spike" in self.__storage:
            self.__storage.remove("Data Spike")
            return True
        return False

    # Apply one hit of damage (can break if threshold reached)
    def take_hit(self):
        self.__damage = self.__damage + 1
        threshold = 2 + self.__upgrade_level
        if self.__damage >= threshold:
            self.__broken = True

    # Return broken state
    def is_broken(self):
        return self.__broken

    # Remove a Removable Drive when extracting
    def consume_removable_drive(self):
        if "Removable Drive" in self.__storage:
            self.__storage.remove("Removable Drive")
            return True
        return False

    # Extract unencrypted Asset objects from rig
    def extract_unsecured_assets(self):
        unsecured = []
        remaining = []
        for item in self.__storage:
            # use check_asset to detect Asset objects
            if check_asset(item):
                if not item.is_encrypted():
                    unsecured.append(item)
                else:
                    remaining.append(item)
            else:
                # keep resource strings like "Data Spike" or "Removable Drive"
                remaining.append(item)
        self.__storage = remaining
        return unsecured

    # Upgrade rig (increase level and storage capacity)
    def upgrade(self):
        self.__upgrade_level = self.__upgrade_level + 1
        self.__storage_limit = self.__storage_limit + 2
        print(self.__name, "was upgraded to level", str(self.__upgrade_level))

    # Repair rig (reset damage and broken state)
    def repair(self):
        self.__damage = 0
        self.__broken = False
        print(self.__name, "has been repaired to pristine state.")

    # Generate a new simple asset (auto asset creation)
    def generate_asset(self):
        new_asset = Asset("generated_" + str(len(self.__storage) + 1), "auto-generated")
        if len(self.__storage) < self.__storage_limit:
            self.__storage.append(new_asset)
            print(self.__name, "generated asset", new_asset.get_name())
        else:
            print(self.__name, "storage full; cannot generate asset.")

    # Accessors
    def get_name(self):
        return self.__name

    def get_storage(self):
        return self.__storage

    def get_upgrade_level(self):
        return self.__upgrade_level

    # Return condition in requested format
    def get_condition(self):
        condition = "Broken" if self.__broken else "Pristine"
        return condition + " (Level " + str(self.__upgrade_level) + ")"

    def __str__(self):
        return self.__name + " - " + self.get_condition() + " - Stored: " + str(len(self.__storage))
