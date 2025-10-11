from Rig import Rig
from Asset import Asset, check_asset

class Hacker:
    def __init__(self, name):
        self.__name = name
        self.__inventory = [Asset("CryptoToken", "Used to acquire or repair rigs.")]
        self.__rig = None
        self.__has_security_chip = True
        self.__trace_level = 0

    # Accessors
    def get_inventory(self):
        return self.__inventory

    def get_rig(self):
        return self.__rig

    def get_trace_level(self):
        return self.__trace_level

    # Trace helpers
    def is_exposed(self):
        return self.__trace_level > 5

    def reduce_trace(self, amount):
        self.__trace_level = self.__trace_level - amount
        if self.__trace_level < 0:
            self.__trace_level = 0
        print(self.__name, "reduced trace to", str(self.__trace_level))

    # Acquire a rig using a CryptoToken
    def acquire_rig(self, rig):
        # Validate that the argument is a Rig instance
        if not isinstance(rig, Rig):
            print("Acquired rig must be a Rig instance.")
            return

        # Find the CryptoToken in inventory (no break)
        token = None
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == "CryptoToken":
                token = item

        # If no token was found
        if token is None:
            print(self.__name, "does not have a CryptoToken to acquire a rig.")
            return

        # Spend the token and assign the rig
        self.__inventory.remove(token)
        self.__rig = rig
        print("Rig '" + rig.get_name() + "' has been activated by hacker " + self.__name + ".")

    # Assign rig without spending token (useful for testing)
    def assign_rig(self, rig):
        if isinstance(rig, Rig):
            self.__rig = rig
            print(self.__name, "assigned rig", rig.get_name())

    # Repair the assigned rig using a CryptoToken
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

    # Launch a Data Spike at another rig
    def launch_data_spike(self, target_rig):
        # block action if exposed
        if self.is_exposed():
            print(self.__name, "is exposed and cannot launch attacks until trace is reduced.")
            return

        # need an attacker rig
        if self.__rig is None:
            print(self.__name, "has no rig to launch data spikes.")
            return

        # consume a data spike from attacker's rig
        if not self.__rig.consume_data_spike():
            print(self.__name, "has no Data Spikes available to launch.")
            return

        # perform the attack
        target_rig.take_hit()

        # increase trace because this is a risky action
        self.__trace_level = self.__trace_level + 1

        # notify when trace crosses the exposure threshold (new message)
        if self.__trace_level > 5:
            print(self.__name, "is now EXPOSED! Actions are blocked until trace is reduced.")

        # friendly readable message instead of True/False
        if target_rig.is_broken():
            print(self.__name, "launched Data Spike at", target_rig.get_name(), "— Rig is now broken!")
        else:
            print(self.__name, "launched Data Spike at", target_rig.get_name(), "— Rig is still functional.")

        # if the target broke, attempt extraction by consuming a removable drive from attacker's rig
        if target_rig.is_broken():
            if self.__rig.consume_removable_drive():
                unsecured = target_rig.extract_unsecured_assets()
                for asset in unsecured:
                    self.__inventory.append(asset)
                print(self.__name, "extracted", str(len(unsecured)), "unsecured assets from", target_rig.get_name())
            else:
                print(self.__name, "has no removable drive to extract assets from", target_rig.get_name())

    # Encrypt an asset in inventory or rig storage
    # Encrypt an asset in inventory or rig storage
    def encrypt_asset(self, asset):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot encrypt assets right now.")
            return
        if not self.__has_security_chip:
            print(self.__name, "has no Security Chip to encrypt.")
            return

        found = False  # Track if we found the asset

        # Search inventory by name
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == asset.get_name():
                item.encrypt()
                print("Encrypted asset:", str(item))
                found = True

        # Search rig storage if hacker has a rig
        if self.__rig is not None:
            for item in self.__rig.get_storage():
                if check_asset(item) and item.get_name() == asset.get_name():
                    item.encrypt()
                    print("Encrypted asset in rig storage:", item.get_name())
                    found = True

        # If not found anywhere, print message
        if not found:
            print("Asset not found in inventory or rig storage; cannot encrypt.")

    # Decrypt an asset in inventory or rig storage
    def decrypt_asset(self, asset):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot decrypt assets right now.")
            return
        if not self.__has_security_chip:
            print(self.__name, "has no Security Chip to decrypt.")
            return

        found = False  # Track if we found the asset

        # Search inventory by name
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == asset.get_name():
                item.decrypt()
                print("Decrypted asset:", str(item))
                found = True

        # Search rig storage if hacker has a rig
        if self.__rig is not None:
            for item in self.__rig.get_storage():
                if check_asset(item) and item.get_name() == asset.get_name():
                    item.decrypt()
                    print("Decrypted asset in rig storage:", item.get_name())
                    found = True

        # If not found anywhere, print message
        if not found:
            print("Asset not found in inventory or rig storage; cannot decrypt.")

    # Upgrade the assigned rig using a "Hardware Patch" string in inventory
    def upgrade_rig(self):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot upgrade rigs right now.")
            return
        if self.__rig is None:
            print(self.__name, "has no rig to upgrade.")
            return

        # Find a Hardware Patch Asset in inventory (search by name)
        patch = None
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == "Hardware Patch":
                patch = item

        if patch is None:
            print("No Hardware Patch found in inventory.")
            return

        # consume the patch and perform upgrade
        self.__inventory.remove(patch)
        self.__rig.upgrade()

    # Store a specific asset from inventory into the assigned rig's storage
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
        # Block transferring encrypted assets
        if check_asset(asset) and asset.is_encrypted():
            print("Cannot store encrypted asset until it is decrypted:", asset.get_name())
            return
        # Try to add to rig
        if self.__rig.add_asset(asset):
            self.__inventory.remove(asset)
            print("Stored asset", asset.get_name(), "into rig storage.")

    # Store all Asset objects from inventory into the rig (respects rig capacity)
    def store_all_assets(self):
        if self.__rig is None:
            print(self.__name, "has no rig to store assets.")
            return
        for item in list(self.__inventory):
            if check_asset(item):
                self.store_asset(item)

    # Retrieve a specific asset from rig storage back into inventory
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

    # Retrieve all unencrypted assets from rig into inventory
    def retrieve_all_from_rig(self):
        if self.__rig is None:
            print(self.__name, "has no rig to retrieve assets from.")
            return
        for item in list(self.__rig.get_storage()):
            if check_asset(item) and not item.is_encrypted():
                self.retrieve_asset(item)

    # Scan inventory for an asset by name, remove and return it if found
    def scan_inventory(self, asset_name):
        for item in list(self.__inventory):
            if check_asset(item) and item.get_name() == asset_name:
                self.__inventory.remove(item)
                print("Scanned and removed asset:", asset_name)
                return item
        print("No asset found by that name in inventory.")
        return None

    # return a readable summary required by the brief
    def __str__(self):
        names = []
        for item in self.__inventory:
            if check_asset(item):
                names.append(item.get_name())
            else:
                names.append(str(item))
        rig_name = self.__rig.get_name() if self.__rig else "None"
        return "Hacker: " + self.__name + " | Rig: " + rig_name + " | Trace Level: " + str(self.__trace_level) + " | Inventory: " + str(names)
