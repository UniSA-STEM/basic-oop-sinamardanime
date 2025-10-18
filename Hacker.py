"""
File: Hacker.py
Description: This file defines the Hacker class used in the 'Into the Grid' system. It represents
a hacker who can use rigs, manage assets, and perform actions like attacking, upgrading,
encrypting, and repairing. The class controls how hackers interact with rigs and assets
through their inventory and trace system.

Author: Sina Mardani Mehrabad
ID: Marsyl127
Username: sinamardanime
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from Rig import Rig

# check_asset checks whether the provided object is an instance of the Asset class. Used throughout the program to
# safely confirm that an object is a valid Asset type.
from Asset import Asset, check_asset


"""
File: Hacker.py
Description: This file defines the Hacker class used in the 'Into the Grid' system. It represents
a hacker who can use rigs, manage assets, and perform actions like attacking, upgrading,
encrypting, and repairing. The class controls how hackers interact with rigs and assets
through their inventory and trace system.

Author: Sina Mardani Mehrabad
ID: Marsyl127
Username: sinamardanime
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Rig import Rig
from Asset import Asset, check_asset


class Hacker:
    """
    Description: Represents a hacker who can acquire rigs, manage assets,
    perform encryption, attack other rigs, and repair or upgrade their equipment.
    Parameters: name – The hacker’s alias or display name.
    Returns: None. Initialises inventory, rig, and trace attributes.
    """

    """
    Description: Initialises a new Hacker with a name, basic inventory (CryptoToken),
    and base attributes like trace level and security chip.
    Parameters: name – string, hacker’s alias.
    Returns: None.
    """
    def __init__(self, name):
        self.__name = name  # stores the hacker’s name
        self.__inventory = [Asset("CryptoToken", "Used to acquire or repair rigs.")]  # ensures hacker starts with one CryptoToken
        self.__rig = None  # tracks assigned rig; starts with None
        self.__has_security_chip = True  # ensures hacker owns a Security Chip by default
        self.__trace_level = 0  # sets starting trace level to 0 (hidden state)

    """
    Description: Returns the list of assets currently in the hacker's inventory.
    Parameters: None.
    Returns: A list of Asset objects representing the hacker’s inventory.
    """
    def get_inventory(self):
        return self.__inventory  # returns all assets currently held

    """
    Description: Returns the Rig object currently assigned to the hacker.
    Parameters: None.
    Returns: The hacker’s assigned Rig object, or None if no rig is set.
    """
    def get_rig(self):
        return self.__rig  # returns the current rig if assigned

    """
    Description: Updates the hacker's name.
    Parameters: new_name – string, the new name for the hacker.
    Returns: None.
    """
    def set_name(self, new_name):
        self.__name = new_name  # updates the hacker’s display name

    """
    Description: Assigns a new rig to the hacker (or removes one if None is passed).
    Parameters: new_rig – Rig object or None.
    Returns: None. Prints warning if invalid type.
    """
    def set_rig(self, new_rig):
        if isinstance(new_rig, Rig) or new_rig is None:  # checks if rig is valid or None
            self.__rig = new_rig  # assigns or clears rig safely
        else:
            print("Invalid rig assignment.")  # prevents invalid rig assignment

    """
    Description: Returns the hacker’s current trace level.
    Parameters: None.
    Returns: Integer – the hacker’s trace level.
    """
    def get_trace_level(self):
        return self.__trace_level  # returns hacker’s trace level value

    """
    Description: Checks if the hacker is currently exposed.
    A hacker becomes exposed when trace level > 5.
    Parameters: None.
    Returns: True if trace level > 5, otherwise False.
    """
    def is_exposed(self):
        return self.__trace_level > 5  # checks whether hacker is exposed

    """
    Description: Reduces the hacker’s trace level by a specific amount, never going below 0.
    Parameters: amount – integer amount to reduce.
    Returns: None. Prints updated trace level.
    """
    def reduce_trace(self, amount):
        self.__trace_level -= amount  # decreases trace
        if self.__trace_level < 0:  # ensures trace cannot go negative
            self.__trace_level = 0
        print(self.__name, "reduced trace to", str(self.__trace_level))  # shows updated trace level

    """
    Description: Lets the hacker buy and activate a rig using a CryptoToken.
    Validates the rig, checks inventory for a CryptoToken, removes it, and assigns the rig.
    Parameters: rig – Rig object to acquire.
    Returns: None. Prints result.
    """
    def acquire_rig(self, rig):
        if not isinstance(rig, Rig):  # ensures provided rig is a valid Rig object
            print("Acquired rig must be a Rig instance.")
            return

        token = None  # placeholder for CryptoToken asset

        # checks if hacker has a CryptoToken in inventory
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == "CryptoToken":
                token = item  # found valid token

        if token is None:  # prevents rig purchase if no token exists
            print(self.__name, "does not have a CryptoToken to acquire a rig.")
            return

        self.__inventory.remove(token)  # removes the token to simulate spending
        self.__rig = rig  # assigns the new rig to the hacker
        print("Rig '" + rig.get_name() + "' has been activated by hacker " + self.__name + ".")  # confirms action

    """
    Description: Directly assigns a rig to the hacker without using a CryptoToken.
    Parameters: rig – Rig object.
    Returns: None.
    """
    def assign_rig(self, rig):
        if isinstance(rig, Rig):  # ensures rig is valid
            self.__rig = rig  # assigns rig
            print(self.__name, "assigned rig", rig.get_name())  # confirms rig assignment

    """
    Description: Repairs the hacker’s rig using a CryptoToken from inventory.
    Ensures the hacker has a rig and CryptoToken before repairing.
    Parameters: None.
    Returns: None.
    """
    def repair_rig(self):
        if self.__rig is None:  # ensures hacker has a rig to repair
            print(self.__name, "has no rig to repair.")
            return

        token = None  # token placeholder
        for item in self.__inventory:  # searches for CryptoToken
            if check_asset(item) and item.get_name() == "CryptoToken":
                token = item

        if token is None:  # prevents repair if no token exists
            print(self.__name, "has no CryptoToken to repair the rig.")
            return

        self.__inventory.remove(token)  # removes token from inventory
        self.__rig.repair()  # repairs the rig

    """
    Description: Launches a Data Spike attack from the hacker’s rig at a target rig.
    Parameters: target_rig – Rig object to attack.
    Returns: None. Prints battle results.
    """
    def launch_data_spike(self, target_rig):
        if self.is_exposed():  # prevents attack if hacker is exposed
            print(self.__name, "is exposed and cannot launch attacks until trace is reduced.")
            return

        if self.__rig is None:  # ensures hacker has a rig
            print(self.__name, "has no rig to launch data spikes.")
            return

        if not self.__rig.consume_data_spike():  # ensures Data Spike exists
            print(self.__name, "has no Data Spikes available to launch.")
            return

        target_rig.take_hit()  # applies one hit of damage to the target rig
        self.__trace_level += 1  # increases trace level after attack

        if self.__trace_level > 5:  # checks if hacker is now exposed
            print(self.__name, "is now EXPOSED! Actions are blocked until trace is reduced.")

        # reports the condition of the target rig after attack
        if target_rig.is_broken():
            print(self.__name, "launched Data Spike at", target_rig.get_name(), "— Rig is now broken!")
        else:
            print(self.__name, "launched Data Spike at", target_rig.get_name(), "— Rig is still functional.")

        # handles extraction of assets if target rig is broken
        if target_rig.is_broken():
            if self.__rig.consume_removable_drive():  # ensures a removable drive is available
                unsecured = target_rig.extract_unsecured_assets()  # retrieves unencrypted assets
                for asset in unsecured:
                    self.__inventory.append(asset)  # adds extracted assets to hacker’s inventory
                print(self.__name, "extracted", str(len(unsecured)), "unsecured assets from", target_rig.get_name())
            else:
                print(self.__name, "has no removable drive to extract assets from", target_rig.get_name())

    """
    Description: Encrypts an asset found in inventory or rig storage if not exposed.
    Parameters: asset – Asset object to encrypt.
    Returns: None.
    """
    def encrypt_asset(self, asset):
        if self.is_exposed():  # prevents encryption if hacker is exposed
            print(self.__name, "is exposed and cannot encrypt assets right now.")
            return
        if not self.__has_security_chip:  # ensures hacker has security chip
            print(self.__name, "has no Security Chip to encrypt.")
            return

        found = False  # tracks if asset is located
        for item in self.__inventory:  # searches inventory for asset
            if check_asset(item) and item.get_name() == asset.get_name():
                item.encrypt()  # encrypts the asset
                print("Encrypted asset:", str(item))
                found = True

        if self.__rig is not None:  # also searches rig storage if available
            for item in self.__rig.get_storage():
                if check_asset(item) and item.get_name() == asset.get_name():
                    item.encrypt()
                    print("Encrypted asset in rig storage:", item.get_name())
                    found = True

        if not found:  # handles case where asset doesn’t exist
            print("Asset not found in inventory or rig storage; cannot encrypt.")

    """
    Description: Decrypts an asset found in inventory or rig storage if not exposed.
    Parameters: asset – Asset object to decrypt.
    Returns: None.
    """
    def decrypt_asset(self, asset):
        if self.is_exposed():  # prevents decryption if hacker is exposed
            print(self.__name, "is exposed and cannot decrypt assets right now.")
            return
        if not self.__has_security_chip:  # ensures hacker has a Security Chip
            print(self.__name, "has no Security Chip to decrypt.")
            return

        found = False  # tracks if asset is found
        for item in self.__inventory:  # searches hacker’s inventory
            if check_asset(item) and item.get_name() == asset.get_name():
                item.decrypt()  # decrypts asset
                print("Decrypted asset:", str(item))
                found = True

        if self.__rig is not None:  # also checks rig storage
            for item in self.__rig.get_storage():
                if check_asset(item) and item.get_name() == asset.get_name():
                    item.decrypt()
                    print("Decrypted asset in rig storage:", item.get_name())
                    found = True

        if not found:  # prints message if asset not found
            print("Asset not found in inventory or rig storage; cannot decrypt.")

    """
    Description: Upgrades the hacker’s rig using a Hardware Patch from inventory.
    Parameters: None.
    Returns: None.
    """
    def upgrade_rig(self):
        if self.is_exposed():  # prevents upgrade while exposed
            print(self.__name, "is exposed and cannot upgrade rigs right now.")
            return
        if self.__rig is None:  # ensures hacker has rig
            print(self.__name, "has no rig to upgrade.")
            return

        patch = None  # placeholder for Hardware Patch
        for item in self.__inventory:  # searches inventory
            if check_asset(item) and item.get_name() == "Hardware Patch":
                patch = item

        if patch is None:  # prevents upgrade if no patch found
            print("No Hardware Patch found in inventory.")
            return

        self.__inventory.remove(patch)  # removes patch
        self.__rig.upgrade()  # upgrades rig

    """
    Description: Stores a specific asset from the hacker’s inventory into their rig storage.
    Parameters: asset – Asset object to store.
    Returns: None.
    """
    def store_asset(self, asset):
        if self.is_exposed():  # prevents storing assets while exposed
            print(self.__name, "is exposed and cannot store assets right now.")
            return
        if self.__rig is None:  # ensures rig is assigned
            print(self.__name, "has no rig to store assets.")
            return
        if asset not in self.__inventory:  # ensures asset exists in inventory
            print("Asset not found in inventory.")
            return
        if check_asset(asset) and asset.is_encrypted():  # prevents storing encrypted items
            print("Cannot store encrypted asset until it is decrypted:", asset.get_name())
            return

        if self.__rig.add_asset(asset):  # adds asset to rig storage
            self.__inventory.remove(asset)  # removes from inventory after transfer
            print("Stored asset", asset.get_name(), "into rig storage.")

    """
    Description: Stores all asset objects from the hacker’s inventory into the rig storage.
    Parameters: None.
    Returns: None.
    """
    def store_all_assets(self):
        if self.__rig is None:  # ensures hacker has a rig
            print(self.__name, "has no rig to store assets.")
            return
        for item in list(self.__inventory):  # loops through all assets
            if check_asset(item):  # ensures each is valid Asset
                self.store_asset(item)  # stores each one

    """
    Description: Retrieves a specific asset from the rig’s storage and moves it to inventory.
    Parameters: asset – Asset object to retrieve.
    Returns: None.
    """
    def retrieve_asset(self, asset):
        if self.is_exposed():  # prevents retrieval while exposed
            print(self.__name, "is exposed and cannot retrieve assets right now.")
            return
        if self.__rig is None:  # ensures rig exists
            print(self.__name, "has no rig to retrieve assets from.")
            return
        if asset not in self.__rig.get_storage():  # ensures asset is in rig storage
            print("Asset not found in rig storage.")
            return
        self.__inventory.append(asset)  # moves asset to inventory
        self.__rig.get_storage().remove(asset)  # removes from rig storage
        print("Retrieved asset", asset.get_name(), "from rig storage.")

    """
    Description: Retrieves all unencrypted assets from the rig’s storage into inventory.
    Parameters: None.
    Returns: None.
    """
    def retrieve_all_from_rig(self):
        if self.__rig is None:  # ensures rig exists
            print(self.__name, "has no rig to retrieve assets from.")
            return
        for item in list(self.__rig.get_storage()):  # iterates through stored assets
            if check_asset(item) and not item.is_encrypted():  # retrieves only unencrypted ones
                self.retrieve_asset(item)

    """
    Description: Scans inventory for an asset by name, removes it if found, and returns it.
    Parameters: asset_name – string, the asset’s name to search for.
    Returns: The Asset object if found; otherwise None.
    """
    def scan_inventory(self, asset_name):
        for item in list(self.__inventory):  # iterates through inventory
            if check_asset(item) and item.get_name() == asset_name:  # checks for matching asset
                self.__inventory.remove(item)  # removes it once found
                print("Scanned and removed asset:", asset_name)
                return item
        print("No asset found by that name in inventory.")  # handles not found
        return None

    """
    Description: Returns a readable summary of the hacker’s current status,
    including name, rig, trace level, and inventory contents.
    Parameters: None.
    Returns: String summary.
    """
    def __str__(self):
        names = []  # stores names of assets
        for item in self.__inventory:  # iterates over inventory
            if check_asset(item):
                names.append(item.get_name())  # adds asset name
            else:
                names.append(str(item))  # adds string version
        rig_name = self.__rig.get_name() if self.__rig else "None"  # handles case of no rig
        return "Hacker: " + self.__name + " | Rig: " + rig_name + " | Trace Level: " + str(self.__trace_level) + " | Inventory: " + str(names)
