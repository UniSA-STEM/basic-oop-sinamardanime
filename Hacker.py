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
        self.__name = name
        self.__inventory = [Asset("CryptoToken", "Used to acquire or repair rigs.")]
        self.__rig = None
        self.__has_security_chip = True
        self.__trace_level = 0

    """
    Description: Returns the list of assets currently in the hacker's inventory.
    Parameters: None.
    Returns: A list of Asset objects representing the hacker’s inventory.
    """
    def get_inventory(self):
        return self.__inventory

    """
    Description: Returns the Rig object currently assigned to the hacker.
    Parameters: None.
    Returns: The hacker’s assigned Rig object, or None if no rig is set.
    """
    def get_rig(self):
        return self.__rig

    """
    Description: Updates the hacker's name.
    Parameters: new_name – string, the new name for the hacker.
    Returns: None.
    """
    def set_name(self, new_name):
        self.__name = new_name

    """
    Description: Assigns a new rig to the hacker (or removes one if None is passed).
    Parameters: new_rig – Rig object or None.
    Returns: None. Prints warning if invalid type.
    """
    def set_rig(self, new_rig):
        if isinstance(new_rig, Rig) or new_rig is None:
            self.__rig = new_rig
        else:
            print("Invalid rig assignment.")

    """
    Description: Returns the hacker’s current trace level.
    Parameters: None.
    Returns: Integer – the hacker’s trace level.
    """
    def get_trace_level(self):
        return self.__trace_level

    """
    Description: Checks if the hacker is currently exposed.
    A hacker becomes exposed when trace level > 5.
    Parameters: None.
    Returns: True if trace level > 5, otherwise False.
    """
    def is_exposed(self):
        return self.__trace_level > 5

    """
    Description: Reduces the hacker’s trace level by a specific amount, never going below 0.
    Parameters: amount – integer amount to reduce.
    Returns: None. Prints updated trace level.
    """
    def reduce_trace(self, amount):
        self.__trace_level -= amount
        if self.__trace_level < 0:
            self.__trace_level = 0
        print(self.__name, "reduced trace to", str(self.__trace_level))

    """
    Description: Lets the hacker buy and activate a rig using a CryptoToken.
    Validates the rig, checks inventory for a CryptoToken, removes it, and assigns the rig.
    Parameters: rig – Rig object to acquire.
    Returns: None. Prints result.
    """
    def acquire_rig(self, rig):
        if not isinstance(rig, Rig):
            print("Acquired rig must be a Rig instance.")
            return

        token = None
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == "CryptoToken":
                token = item

        if token is None:
            print(self.__name, "does not have a CryptoToken to acquire a rig.")
            return

        self.__inventory.remove(token)
        self.__rig = rig
        print("Rig '" + rig.get_name() + "' has been activated by hacker " + self.__name + ".")

    """
    Description: Directly assigns a rig to the hacker without using a CryptoToken.
    Parameters: rig – Rig object.
    Returns: None.
    """
    def assign_rig(self, rig):
        if isinstance(rig, Rig):
            self.__rig = rig
            print(self.__name, "assigned rig", rig.get_name())

    """
    Description: Repairs the hacker’s rig using a CryptoToken from inventory.
    Ensures the hacker has a rig and CryptoToken before repairing.
    Parameters: None.
    Returns: None.
    """
    def repair_rig(self):
        if self.__rig is None:
            print(self.__name, "has no rig to repair.")
            return

        token = None
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == "CryptoToken":
                token = item

        if token is None:
            print(self.__name, "has no CryptoToken to repair the rig.")
            return

        self.__inventory.remove(token)
        self.__rig.repair()

    """
    Description: Launches a Data Spike attack from the hacker’s rig at a target rig.
    Parameters: target_rig – Rig object to attack.
    Returns: None. Prints battle results.
    """
    def launch_data_spike(self, target_rig):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot launch attacks until trace is reduced.")
            return

        if self.__rig is None:
            print(self.__name, "has no rig to launch data spikes.")
            return

        if not self.__rig.consume_data_spike():
            print(self.__name, "has no Data Spikes available to launch.")
            return

        target_rig.take_hit()
        self.__trace_level += 1

        if self.__trace_level > 5:
            print(self.__name, "is now EXPOSED! Actions are blocked until trace is reduced.")

        if target_rig.is_broken():
            print(self.__name, "launched Data Spike at", target_rig.get_name(), "— Rig is now broken!")
        else:
            print(self.__name, "launched Data Spike at", target_rig.get_name(), "— Rig is still functional.")

        if target_rig.is_broken():
            if self.__rig.consume_removable_drive():
                unsecured = target_rig.extract_unsecured_assets()
                for asset in unsecured:
                    self.__inventory.append(asset)
                print(self.__name, "extracted", str(len(unsecured)), "unsecured assets from", target_rig.get_name())
            else:
                print(self.__name, "has no removable drive to extract assets from", target_rig.get_name())

    """
    Description: Encrypts an asset found in inventory or rig storage if not exposed.
    Parameters: asset – Asset object to encrypt.
    Returns: None.
    """
    def encrypt_asset(self, asset):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot encrypt assets right now.")
            return
        if not self.__has_security_chip:
            print(self.__name, "has no Security Chip to encrypt.")
            return

        found = False

        for item in self.__inventory:
            if check_asset(item) and item.get_name() == asset.get_name():
                item.encrypt()
                print("Encrypted asset:", str(item))
                found = True

        if self.__rig is not None:
            for item in self.__rig.get_storage():
                if check_asset(item) and item.get_name() == asset.get_name():
                    item.encrypt()
                    print("Encrypted asset in rig storage:", item.get_name())
                    found = True

        if not found:
            print("Asset not found in inventory or rig storage; cannot encrypt.")

    """
    Description: Decrypts an asset found in inventory or rig storage if not exposed.
    Parameters: asset – Asset object to decrypt.
    Returns: None.
    """
    def decrypt_asset(self, asset):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot decrypt assets right now.")
            return
        if not self.__has_security_chip:
            print(self.__name, "has no Security Chip to decrypt.")
            return

        found = False

        for item in self.__inventory:
            if check_asset(item) and item.get_name() == asset.get_name():
                item.decrypt()
                print("Decrypted asset:", str(item))
                found = True

        if self.__rig is not None:
            for item in self.__rig.get_storage():
                if check_asset(item) and item.get_name() == asset.get_name():
                    item.decrypt()
                    print("Decrypted asset in rig storage:", item.get_name())
                    found = True

        if not found:
            print("Asset not found in inventory or rig storage; cannot decrypt.")

    """
    Description: Upgrades the hacker’s rig using a Hardware Patch from inventory.
    Parameters: None.
    Returns: None.
    """
    def upgrade_rig(self):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot upgrade rigs right now.")
            return
        if self.__rig is None:
            print(self.__name, "has no rig to upgrade.")
            return

        patch = None
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == "Hardware Patch":
                patch = item

        if patch is None:
            print("No Hardware Patch found in inventory.")
            return

        self.__inventory.remove(patch)
        self.__rig.upgrade()

    """
    Description: Stores a specific asset from the hacker’s inventory into their rig storage.
    Parameters: asset – Asset object to store.
    Returns: None.
    """
    def store_asset(self, asset):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot store assets right now.")
            return
        if self.__rig is None:
            print(self.__name, "has no rig to store assets.")
            return
        if asset not in self.__inventory:
            print("Asset not found in inventory.")
            return
        if check_asset(asset) and asset.is_encrypted():
            print("Cannot store encrypted asset until it is decrypted:", asset.get_name())
            return

        if self.__rig.add_asset(asset):
            self.__inventory.remove(asset)
            print("Stored asset", asset.get_name(), "into rig storage.")

    """
    Description: Stores all asset objects from the hacker’s inventory into the rig storage.
    Parameters: None.
    Returns: None.
    """
    def store_all_assets(self):
        if self.__rig is None:
            print(self.__name, "has no rig to store assets.")
            return
        for item in list(self.__inventory):
            if check_asset(item):
                self.store_asset(item)

    """
    Description: Retrieves a specific asset from the rig’s storage and moves it to inventory.
    Parameters: asset – Asset object to retrieve.
    Returns: None.
    """
    def retrieve_asset(self, asset):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot retrieve assets right now.")
            return
        if self.__rig is None:
            print(self.__name, "has no rig to retrieve assets from.")
            return
        if asset not in self.__rig.get_storage():
            print("Asset not found in rig storage.")
            return
        self.__inventory.append(asset)
        self.__rig.get_storage().remove(asset)
        print("Retrieved asset", asset.get_name(), "from rig storage.")

    """
    Description: Retrieves all unencrypted assets from the rig’s storage into inventory.
    Parameters: None.
    Returns: None.
    """
    def retrieve_all_from_rig(self):
        if self.__rig is None:
            print(self.__name, "has no rig to retrieve assets from.")
            return
        for item in list(self.__rig.get_storage()):
            if check_asset(item) and not item.is_encrypted():
                self.retrieve_asset(item)

    """
    Description: Scans inventory for an asset by name, removes it if found, and returns it.
    Parameters: asset_name – string, the asset’s name to search for.
    Returns: The Asset object if found; otherwise None.
    """
    def scan_inventory(self, asset_name):
        for item in list(self.__inventory):
            if check_asset(item) and item.get_name() == asset_name:
                self.__inventory.remove(item)
                print("Scanned and removed asset:", asset_name)
                return item
        print("No asset found by that name in inventory.")
        return None

    """
    Description: Returns a readable summary of the hacker’s current status,
    including name, rig, trace level, and inventory contents.
    Parameters: None.
    Returns: String summary.
    """
    def __str__(self):
        names = []
        for item in self.__inventory:
            if check_asset(item):
                names.append(item.get_name())
            else:
                names.append(str(item))
        rig_name = self.__rig.get_name() if self.__rig else "None"
        return "Hacker: " + self.__name + " | Rig: " + rig_name + " | Trace Level: " + str(self.__trace_level) + " | Inventory: " + str(names)
