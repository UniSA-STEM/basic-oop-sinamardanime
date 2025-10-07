"""
File: Hacker.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from Rig import Rig
from Asset import Asset

class Hacker:
    def __init__(self, name):
        self.__name = name
        self.__inventory = ["CryptoToken"]  # starts with one token
        self.__rig = None                   # no rig at start
        self.__has_security_chip = True     # assume they have a security chip
        self.__trace_level = 0              # trace level starts at 0

    # Return inventory list
    def get_inventory(self):
        return self.__inventory

    # Return the rig
    def get_rig(self):
        return self.__rig

    # Return trace level
    def get_trace_level(self):
        return self.__trace_level

    # Acquire a rig using a CryptoToken
    def acquire_rig(self, rig):
        if not isinstance(rig, Rig):
            print("Rig must be a Rig object.")
            return
        if "CryptoToken" not in self.__inventory:
            print(self.__name, "has no CryptoToken to buy rig.")
            return
        self.__inventory.remove("CryptoToken")
        self.__rig = rig
        print("Rig '" + rig.get_name() + "' activated for", self.__name)

    # Assign rig without using CryptoToken (for testing)
    def assign_rig(self, rig):
        if isinstance(rig, Rig):
            self.__rig = rig
            print(self.__name, "assigned rig", rig.get_name())

    # Launch data spike attack
    def launch_data_spike(self, target_rig):
        if self.__rig is None:
            print(self.__name, "has no rig to attack.")
            return
        if not isinstance(target_rig, Rig):
            print("Target is not a rig.")
            return
        if not self.__rig.consume_data_spike():
            print(self.__name, "has no data spikes left.")
            return

        target_rig.take_hit()
        self.__trace_level = self.__trace_level + 1
        print(self.__name, "launched Data Spike at", target_rig.get_name(), "Broken:", target_rig.is_broken())

        if target_rig.is_broken():
            if self.__rig.consume_removable_drive():
                unsecured = target_rig.extract_unsecured_assets()
                for asset in unsecured:
                    self.__inventory.append(asset)
                print(self.__name, "extracted", str(len(unsecured)), "unsecured assets from", target_rig.get_name())
            else:
                print(self.__name, "has no removable drive to extract assets.")

    # Encrypt asset in inventory or rig storage
    def encrypt_asset(self, asset):
        if not self.__has_security_chip:
            print("No Security Chip available.")
            return
        if asset in self.__inventory:
            asset.encrypt()
            print("Encrypted asset:", asset.get_name())
            return
        if self.__rig is not None and asset in self.__rig.get_storage():
            asset.encrypt()
            print("Encrypted asset in rig:", asset.get_name())
            return
        print("Asset not found to encrypt.")

    # Decrypt asset in inventory or rig storage
    def decrypt_asset(self, asset):
        if not self.__has_security_chip:
            print("No Security Chip available.")
            return
        if asset in self.__inventory:
            asset.decrypt()
            print("Decrypted asset:", asset.get_name())
            return
        if self.__rig is not None and asset in self.__rig.get_storage():
            asset.decrypt()
            print("Decrypted asset in rig:", asset.get_name())
            return
        print("Asset not found to decrypt.")

    # Upgrade rig with a Hardware Patch
    def upgrade_rig(self):
        if self.__rig is None:
            print("No rig to upgrade.")
            return
        if "Hardware Patch" not in self.__inventory:
            print("No Hardware Patch available.")
            return
        self.__inventory.remove("Hardware Patch")
        self.__rig.upgrade()

    # Store asset into rig
    def store_asset(self, asset):
        if self.__rig is None:
            print("No rig available.")
            return
        if asset not in self.__inventory:
            print("Asset not found in inventory.")
            return
        self.__rig.add_asset(asset)
        if asset in self.__rig.get_storage():
            self.__inventory.remove(asset)
            print("Stored asset", asset.get_name(), "into rig.")

    # Retrieve asset from rig back into inventory
    def retrieve_asset(self, asset):
        if self.__rig is None:
            print("No rig to retrieve from.")
            return
        if asset not in self.__rig.get_storage():
            print("Asset not found in rig.")
            return
        self.__inventory.append(asset)
        self.__rig.get_storage().remove(asset)
        print("Retrieved asset", asset.get_name(), "from rig.")

    # Scan inventory for an asset by name and remove it
    def scan_inventory(self, name):
        for item in self.__inventory:
            if hasattr(item, "get_name") and item.get_name() == name:
                self.__inventory.remove(item)
                print("Scanned and removed asset:", name)
                return item
        print("No asset found named", name)
        return None

    # Print hacker info
    def __str__(self):
        names = []
        for item in self.__inventory:
            if hasattr(item, "get_name"):
                names.append(item.get_name())
            else:
                names.append(str(item))
        rig_name = self.__rig.get_name() if self.__rig else "None"
        return "Hacker: " + self.__name + " | Rig: " + rig_name + " | Trace Level: " + str(self.__trace_level) + " | Inventory: " + str(names)