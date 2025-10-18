"""
File: Rig.py
Description: This file defines the Rig class for the system. A rig represents a hacker’s
computer that stores assets, takes damage, and can be upgraded or repaired. It starts with
basic items like Data Spikes and a Removable Drive and supports actions such as taking hits,
extracting assets, and generating new ones.

Author: Sina Mardani Mehrabad
ID: Marsyl127
Username: sinamardanime
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Asset import Asset, check_asset

# Description: Represents a hacker’s rig device which stores assets, handles upgrades, damage, repairs, and extraction operations.
# Parameters: name – the name of the rig instance.
# Returns: None. Initialises default storage, upgrade level, and damage state.
class Rig:
    def __init__(self, name):
            self.__name = name
            # Initial rig storage with some default assets and resources
            self.__storage = [
                Asset("Data Spike", "Used in battles."),
                Asset("Data Spike", "Used in battles."),
                Asset("Removable Drive", "Used for extraction.")
            ]
            self.__damage = 0
            self.__broken = False
            self.__upgrade_level = 0
            self.__storage_limit = 5

    # Updates the rig’s name.
    # Parameters: new_name – new name for the rig.
    def set_name(self, new_name):
        self.__name = new_name

    # Updates the rig’s upgrade level.
    # Parameters: level – integer upgrade level.
    def set_upgrade_level(self, level):
        if level >= 0:
            self.__upgrade_level = level
        else:
            print("Invalid upgrade level; must be non-negative.")

    # Updates the storage limit of the rig.
    # Parameters: limit – integer storage capacity.
    def set_storage_limit(self, limit):
        if limit > 0:
            self.__storage_limit = limit
        else:
            print("Storage limit must be positive.")



    # Description: Adds an asset to the rig’s storage if space is available.
    # Parameters: asset – the asset object to add to the rig’s storage.
    # Returns: True if successfully added, False if storage is full.
    def add_asset(self, asset):
        # Check if storage is at maximum capacity
        if len(self.__storage) >= self.__storage_limit:
            print("Cannot add asset; storage full for rig", self.__name)
            return False
        self.__storage.append(asset)
        return True

    # Description: Consumes a Data Spike resource from the rig’s storage which is used in attacks.
    # Parameters: None.
    # Returns: True if a Data Spike was found and removed, False otherwise.
    def consume_data_spike(self):
        for item in self.__storage:
            if check_asset(item) and item.get_name() == "Data Spike":
                self.__storage.remove(item)
                return True
        return False

    # Description: Applies one hit of damage to the rig and checks if it becomes broken.
    # Parameters: None.
    # Returns: None. Updates the rig’s damage state and broken status.
    def take_hit(self):
        self.__damage = self.__damage + 1
        threshold = 2 + self.__upgrade_level
        if self.__damage >= threshold:
            self.__broken = True

    # Description: Checks if the rig is currently broken.
    # Parameters: None.
    # Returns: True if the rig is broken, False otherwise.
    def is_broken(self):
        return self.__broken

    # Description: Consumes a Removable Drive resource from storage that is used for extracting assets.
    # Parameters: None.
    # Returns: True if a Removable Drive was found and removed, False otherwise.
    def consume_removable_drive(self):
        for item in self.__storage:
            if check_asset(item) and item.get_name() == "Removable Drive":
                self.__storage.remove(item)
                return True
        return False

    # Description: Extracts all unencrypted Asset objects from the rig’s storage.
    # Parameters: None.
    # Returns: A list of unsecured (unencrypted) Asset objects removed from the rig.
    def extract_unsecured_assets(self):
        unsecured = [] # Will hold unencrypted assets
        remaining = []  # Holds everything else that stays in storage
        for item in self.__storage:
            # use check_asset to detect Asset objects
            if check_asset(item):
                if not item.is_encrypted():
                    unsecured.append(item)
                else:
                    remaining.append(item)
            else:
                # Update storage to contain only remaining items
                remaining.append(item)
        self.__storage = remaining
        return unsecured

    # Description: Upgrades the rig, increasing its level and storage capacity.
    # Parameters: None.
    # Returns: None. Prints a confirmation message upon successful upgrade.
    def upgrade(self):
        self.__upgrade_level = self.__upgrade_level + 1
        self.__storage_limit = self.__storage_limit + 2
        print(self.__name, "was upgraded to level", str(self.__upgrade_level))

    # Description: Repairs the rig, resetting damage and restoring it from a broken state.
    # Parameters: None.
    # Returns: None. Prints messages describing the result of the repair attempt.
    def repair(self):
        # checks if the rig actually needs repair
        if self.__damage == 0 and not self.__broken:
            print(self.__name, "is already in pristine condition. No repair needed.")
            return

        # Reset damage and mark rig as functional again
        self.__damage = 0
        self.__broken = False
        print(self.__name, "has been repaired to pristine state.")

    # Description: Automatically generates a new asset inside the rig if space allows.
    # Parameters: None.
    # Returns: None. Prints messages describing the generation result.
    def generate_asset(self):
        new_asset = Asset("generated_" + str(len(self.__storage) + 1), "auto-generated")
        # Add new asset only if storage has room
        if len(self.__storage) < self.__storage_limit:
            self.__storage.append(new_asset)
            print(self.__name, "generated asset", new_asset.get_name())
        else:
            print(self.__name, "storage full; cannot generate asset.")

    # Description: Returns the name of the rig.
    # Parameters: None.
    # Returns: String containing the rig’s name.
    def get_name(self):
        return self.__name

    # Description: Provides access to the list of items currently stored in the rig.
    # Parameters: None.
    # Returns: A list containing all assets and resources stored in the rig.
    def get_storage(self):
        return self.__storage

    # Description: Retrieves the current upgrade level of the rig.
    # Parameters: None.
    # Returns: Integer representing the rig’s upgrade level.
    def get_upgrade_level(self):
        return self.__upgrade_level

    # Description: Returns the rig’s condition (Broken or Pristine) along with its upgrade level.
    # Parameters: None.
    # Returns: String describing the rig’s condition and current upgrade level.
    def get_condition(self):
        condition = "Broken" if self.__broken else "Pristine"
        return condition + " (Level " + str(self.__upgrade_level) + ")"

    # Description: Returns a readable string summary of the rig, including its name, condition, and number of stored items.
    # Parameters: None.
    # Returns: Formatted string summarizing the rig’s status and storage count.
    def __str__(self):
        return self.__name + " - " + self.get_condition() + " - Stored: " + str(len(self.__storage))
