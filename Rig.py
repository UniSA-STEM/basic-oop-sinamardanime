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


class Rig:
    """
    Description: Represents a hacker’s rig device which stores assets, handles upgrades,
    damage, repairs, and extraction operations.
    Parameters: name – the name of the rig instance.
    Returns: None. Initialises default storage, upgrade level, and damage state.
    """

    """
    Description: Initialises the rig with default storage, upgrade level, and damage state.
    Parameters: name – string, name of the rig instance.
    Returns: None.
    """
    def __init__(self, name):
        self.name = name
        self.__storage = [
            Asset("Data Spike", "Used in battles."),
            Asset("Data Spike", "Used in battles."),
            Asset("Removable Drive", "Used for extraction.")
        ]  # Default items inside the rig

        self.__damage = 0            # Tracks how many hits the rig has taken
        self.__broken = False        # True if the rig is currently broken
        self.__upgrade_level = 0     # The current upgrade level
        self.__storage_limit = 5     # The maximum number of assets the rig can hold

    """
    Description: Updates the rig’s name.
    Parameters: new_name – new name for the rig.
    Returns: None.
    """
    def set_name(self, new_name):
        # Checks that the new name is a string (not a number or other type)
        if isinstance(new_name, str):
            # Ensures the string is not empty or made of only spaces
            if new_name.strip() != "":
                self.__name = new_name  # Assigns a valid name to the rig
            else:
                print("Error: Rig name cannot be empty. Defaulting to 'Unnamed_Rig'.")
                self.__name = "Unnamed_Rig"  # Assigns default if blank
        else:
            print("Error: Invalid rig name type. Expected a string. Defaulting to 'Unnamed_Rig'.")
            self.__name = "Unnamed_Rig"  # Assigns default if invalid type


    """
    Description: Updates the rig’s storage limit.
    Parameters: limit – integer, the new maximum storage capacity.
    Returns: None. Prints warning if invalid.
    """
    def set_storage_limit(self, limit):
        if limit > 0:
            self.__storage_limit = limit  # Apply new limit
        else:
            print("Storage limit must be positive.")

    """
    Description: Adds an asset to the rig’s storage if space is available.
    Parameters: asset – Asset object to be added.
    Returns: True if successfully added, False if storage is full.
    """
    def add_asset(self, asset):
        if len(self.__storage) >= self.__storage_limit:  # Check if rig is full
            print("Cannot add asset; storage full for rig", self.__name)
            return False
        self.__storage.append(asset)  # Add asset to storage
        return True

    """
    Description: Consumes a Data Spike resource from the rig’s storage which is used in attacks.
    Parameters: None.
    Returns: True if a Data Spike was found and removed, False otherwise.
    """
    def consume_data_spike(self):
        for item in self.__storage:
            if check_asset(item) and item.get_name() == "Data Spike":
                self.__storage.remove(item)  # Remove one Data Spike
                return True
        return False  # None found

    """
    Description: Applies one hit of damage to the rig and checks if it becomes broken.
    Parameters: None.
    Returns: None. Updates damage and broken status.
    """
    def take_hit(self):
        self.__damage += 1  # Increase damage counter by 1
        threshold = 2 + self.__upgrade_level  # Stronger rigs handle more hits
        if self.__damage >= threshold:
            self.__broken = True  # Rig becomes broken when threshold reached

    """
    Description: Checks if the rig is currently broken.
    Parameters: None.
    Returns: True if the rig is broken, False otherwise.
    """
    def is_broken(self):
        return self.__broken

    """
    Description: Consumes a Removable Drive from storage, used for extracting assets.
    Parameters: None.
    Returns: True if a Removable Drive was found and removed, False otherwise.
    """
    def consume_removable_drive(self):
        for item in self.__storage:
            if check_asset(item) and item.get_name() == "Removable Drive":
                self.__storage.remove(item)  # Remove one Removable Drive
                return True
        return False

    """
    Description: Extracts all unencrypted assets from the rig’s storage.
    Parameters: None.
    Returns: A list of unsecured (unencrypted) Asset objects removed from the rig.
    """
    def extract_unsecured_assets(self):
        unsecured = []  # List for unencrypted assets
        remaining = []  # List for encrypted or other items

        for item in self.__storage:
            if check_asset(item):
                if not item.is_encrypted():
                    unsecured.append(item)  # Add to unsecured list
                else:
                    remaining.append(item)  # Keep encrypted assets
            else:
                remaining.append(item)  # Non-asset items stay
        self.__storage = remaining  # Update rig’s storage
        return unsecured

    """
    Description: Upgrades the rig, increasing level and storage capacity.
    Parameters: None.
    Returns: None. Prints confirmation message.
    """
    def upgrade(self):
        self.__upgrade_level += 1       # Level up the rig
        self.__storage_limit += 2       # Increase storage capacity
        print(self.__name, "was upgraded to level", str(self.__upgrade_level))

    """
    Description: Repairs the rig by resetting damage and restoring it from a broken state.
    Parameters: None.
    Returns: None. Prints messages describing the repair outcome.
    """
    def repair(self):
        if self.__damage == 0 and not self.__broken:
            print(self.__name, "is already in pristine condition. No repair needed.")
            return
        self.__damage = 0       # Reset damage
        self.__broken = False   # Mark as repaired
        print(self.__name, "has been repaired to pristine state.")

    """
    Description: Automatically generates a new asset in the rig if space allows.
    Parameters: None.
    Returns: None. Prints messages describing generation outcome.
    """
    def generate_asset(self):
        new_asset = Asset("generated_" + str(len(self.__storage) + 1), "auto-generated")
        if len(self.__storage) < self.__storage_limit:
            self.__storage.append(new_asset)  # Add asset
            print(self.__name, "generated asset", new_asset.get_name())
        else:
            print(self.__name, "storage full; cannot generate asset.")

    """
    Description: Returns the name of the rig.
    Parameters: None.
    Returns: String containing the rig’s name.
    """
    def get_name(self):
        return self.__name

    # Connects the getter and setter as a property
    name = property(get_name, set_name)

    """
    Description: Provides access to the list of items currently stored in the rig.
    Parameters: None.
    Returns: A list containing all assets and resources stored in the rig.
    """
    def get_storage(self):
        return self.__storage

    """
    Description: Retrieves the current upgrade level of the rig.
    Parameters: None.
    Returns: Integer representing the rig’s upgrade level.
    """
    def get_upgrade_level(self):
        return self.__upgrade_level

    """
    Description: Returns the rig’s condition (Broken or Pristine) along with its upgrade level.
    Parameters: None.
    Returns: String describing the rig’s condition and current upgrade level.
    """
    def get_condition(self):
        condition = "Broken" if self.__broken else "Pristine"
        return condition + " (Level " + str(self.__upgrade_level) + ")"

    """
    Description: Returns a readable string summary of the rig, including its name, condition, and number of stored items.
    Parameters: None.
    Returns: Formatted string summarizing the rig’s status and storage count.
    """
    def __str__(self):
        return self.__name + " - " + self.get_condition() + " - Stored: " + str(len(self.__storage))
