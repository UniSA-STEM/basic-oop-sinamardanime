"""
File: Hacker.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""
# hacker.py
# Step-by-step Hacker class. Each line has a short comment explaining it.

# Import Rig and Asset types so we can check types and interact with rigs/assets.
from rig import Rig
from asset import Asset

# Define the Hacker class
class Hacker:

    # Constructor: runs when you make a new Hacker("Name")
    def __init__(self, name):
        # store the hacker's name privately
        self.__name = name

        # inventory holds strings (like "CryptoToken") and Asset objects
        # start with one CryptoToken as the brief says
        self.__inventory = ["CryptoToken"]

        # reference to the hacker's rig; None until assigned
        self.__rig = None

        # model possession of a Security Chip as a boolean (needed for encrypt/decrypt)
        self.__has_security_chip = True

        # trace level starts at 0 (increases when risky actions occur)
        self.__trace_level = 0


    # Return the internal inventory list (you requested direct access)
    def get_inventory(self):
        return self.__inventory


    # Return the rig object currently assigned to this hacker
    def get_rig(self):
        return self.__rig


    # Return current trace level
    def get_trace_level(self):
        return self.__trace_level


    # Assign a rig object to this hacker (no cost)
    def assign_rig(self, rig):
        if isinstance(rig, Rig):
            self.__rig = rig
            # simple confirmation print
            print(self.__name, "assigned rig", rig.get_name())
        else:
            # if not a Rig instance, do nothing (keeps code simple)
            print("Provided object is not a Rig.")


    # Acquire a rig by spending a CryptoToken (if present)
    def acquire_rig(self, rig):
        # check token exists
        if "CryptoToken" not in self.__inventory:
            print(self.__name, "does not have a CryptoToken to acquire a rig.")
            return
        # check rig is a Rig instance
        if not isinstance(rig, Rig):
            print("Acquired rig must be a Rig instance.")
            return
        # remove one CryptoToken and assign the rig
        self.__inventory.remove("CryptoToken")
        self.__rig = rig
        print("Rig '" + rig.get_name() + "' has been activated by hacker " + self.__name + ".")


    # Launch a Data Spike at another rig (target_rig must be Rig)
    def launch_data_spike(self, target_rig):
        # ensure attacker has a rig
        if self.__rig is None:
            print(self.__name, "has no rig to launch a data spike.")
            return

        # ensure target is a Rig
        if not isinstance(target_rig, Rig):
            print("Target is not a rig.")
            return

        # consume one Data Spike from attacker's rig
        if not self.__rig.consume_data_spike():
            print(self.__name, "has no Data Spikes left to attack.")
            return

        # inflict damage on the target rig
        target_rig.take_hit()

        # increase attacker's trace level because this is risky
        self.__trace_level = self.__trace_level + 1

        # report the outcome
        print(self.__name, "launched a Data Spike at", target_rig.get_name() + ". Target broken:", target_rig.is_broken())

        # if the target became broken, attempt extraction
        if target_rig.is_broken():
            # consume one removable drive from attacker's rig to extract
            if self.__rig.consume_removable_drive():
                # get all unsecured (unencrypted) assets from target
                unsecured = target_rig.extract_unsecured_assets()
                # transfer each unsecured asset into attacker's inventory
                for asset in unsecured:
                    self.__inventory.append(asset)
                # report extraction count
                print(self.__name, "extracted", str(len(unsecured)), "unsecured assets from", target_rig.get_name() + ".")
            else:
                # no removable drive available
                print(self.__name, "has no removable drive to extract assets from", target_rig.get_name() + ".")


    # Encrypt an asset that is either in inventory or in the hacker's rig storage
    def encrypt_asset(self, asset):
        # must have a Security Chip to encrypt
        if not self.__has_security_chip:
            print(self.__name, "has no Security Chip to encrypt.")
            return

        # if the exact asset object is in inventory, encrypt it
        if asset in self.__inventory:
            asset.encrypt()
            print("Encrypted asset in inventory:", asset.get_name())
            return

        # if asset is in rig storage, encrypt it there
        if self.__rig is not None and asset in self.__rig.get_storage():
            asset.encrypt()
            print("Encrypted asset in rig storage:", asset.get_name())
            return

        # asset not found anywhere accessible
        print("Asset not found in inventory or rig storage; cannot encrypt.")


    # Decrypt an asset that is either in inventory or in the hacker's rig storage
    def decrypt_asset(self, asset):
        # must have a Security Chip to decrypt
        if not self.__has_security_chip:
            print(self.__name, "has no Security Chip to decrypt.")
            return

        # decrypt if in inventory
        if asset in self.__inventory:
            asset.decrypt()
            print("Decrypted asset in inventory:", asset.get_name())
            return

        # decrypt if in rig storage
        if self.__rig is not None and asset in self.__rig.get_storage():
            asset.decrypt()
            print("Decrypted asset in rig storage:", asset.get_name())
            return

        # asset not found
        print("Asset not found in inventory or rig storage; cannot decrypt.")


    # Upgrade the rig using a "Hardware Patch" string in inventory
    def upgrade_rig(self):
        # must have a rig to upgrade
        if self.__rig is None:
            print(self.__name, "has no rig to upgrade.")
            return
        # must have a Hardware Patch in inventory
        if "Hardware Patch" not in self.__inventory:
            print("No Hardware Patch found in inventory.")
            return
        # consume the Hardware Patch and call rig.upgrade()
        self.__inventory.remove("Hardware Patch")
        self.__rig.upgrade()


    # Store a specific asset from inventory into the assigned rig's storage
    def store_asset(self, asset):
        # need a rig to store into
        if self.__rig is None:
            print(self.__name, "has no rig to store assets.")
            return
        # asset must be present in inventory
        if asset not in self.__inventory:
            print("Asset not found in inventory.")
            return
        # ask rig to add it (rig enforces storage limits)
        self.__rig.add_asset(asset)
        # only remove from inventory if rig actually holds it now
        if asset in self.__rig.get_storage():
            self.__inventory.remove(asset)
            print("Stored asset", asset.get_name(), "into rig storage.")


    # Retrieve a specific asset from rig storage back into inventory
    def retrieve_asset(self, asset):
        # need a rig to retrieve from
        if self.__rig is None:
            print(self.__name, "has no rig to retrieve assets from.")
            return
        # asset must be in rig storage
        if asset not in self.__rig.get_storage():
            print("Asset not found in rig storage.")
            return
        # move it into inventory and remove from rig storage
        self.__inventory.append(asset)
        self.__rig.get_storage().remove(asset)
        print("Retrieved asset", asset.get_name(), "from rig storage.")


    # Scan inventory for an asset by name; if found remove and return it
    def scan_inventory(self, asset_name):
        for item in self.__inventory:
            # check if item is an Asset-like object with get_name method
            if hasattr(item, "get_name") and item.get_name() == asset_name:
                self.__inventory.remove(item)
                print("Scanned and removed asset:", asset_name)
                return item
        # not found
        print("No asset found by that name in inventory.")
        return None


    # __str__ shows a neat summary including trace level as the brief requests
    def __str__(self):
        names = []
        for item in self.__inventory:
            if hasattr(item, "get_name"):
                names.append(item.get_name())
            else:
                names.append(str(item))
        rigname = self.__rig.get_name() if self.__rig else "None"
        return "Hacker: " + self.__name + " | Rig: " + rigname + " | Trace Level: " + str(self.__trace_level) + " | Inventory: " + str(names)

