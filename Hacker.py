from Rig import Rig
# check_asset checks whether the provided object is an instance of the Asset class. Used throughout the program to
# safely confirm that an object is a valid Asset type.

from Asset import Asset, check_asset


# Description:
# Initialises a new Hacker object with a name, starting inventory (1 CryptoToken), and some basic attributes.
# Parameters: name – The hacker’s display name or alias.
# Returns: None
class Hacker:
    def __init__(self, name):
        self.__name = name
        self.__inventory = [Asset("CryptoToken", "Used to acquire or repair rigs.")]
        self.__rig = None
        self.__has_security_chip = True
        self.__trace_level = 0


    # Description: Returns the list of assets currently in the hacker's inventory.
    # Parameters: None
    # Returns: The hacker’s inventory list containing Asset objects.
    def get_inventory(self):
        return self.__inventory

    # Description:  Returns the Rig object currently assigned to the hacker.
    # Parameters: None
    # Returns: The hacker’s assigned Rig, or None if no rig is set.
    def get_rig(self):
        return self.__rig

    # Description: Returns the hacker’s current trace level.
    # Parameters: None
    # Returns: An integer value representing the hacker’s trace level.
    def get_trace_level(self):
        return self.__trace_level

    # Description: Checks whether the hacker is exposed.
    #  A hacker becomes exposed when their trace level exceeds 5.
    # Parameters: None
    # Returns: True if the hacker’s trace level is greater than 5, otherwise False.
    def is_exposed(self):
        return self.__trace_level > 5

    # Description: Reduces the hacker’s trace level by a specific amount.
    # Trace cannot go below 0.
    # Parameters: amount is the number by which to reduce the trace level.
    # Returns: None
    def reduce_trace(self, amount):
        self.__trace_level = self.__trace_level - amount
        if self.__trace_level < 0:
            self.__trace_level = 0
        print(self.__name, "reduced trace to", str(self.__trace_level))

    # Description: Lets the hacker buy and activate a rig using a CryptoToken.
    # Validates the rig, checks for a token in inventory, removes it, and assigns the rig to the hacker.
    # Parameters: rig – The Rig object the hacker wants to acquire.
    # Returns: None
    def acquire_rig(self, rig):
        # ensures the given object is a Rig instance and prevents invalid data types or accidental misuse
        if not isinstance(rig, Rig):
            print("Acquired rig must be a Rig instance.")
            return

        # looks for a CryptoToken in the hacker's inventory as tokens are required as the "currency" for rig acquisition
        token = None
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == "CryptoToken":
                token = item

        # stops here if no CryptoToken is found
        # this makes it fair by preventing free rig activation
        if token is None:
            print(self.__name, "does not have a CryptoToken to acquire a rig.")
            return

        # remove the CryptoToken from inventory to simulate spending it
        # without this step, the hacker could reuse the same token indefinitely
        self.__inventory.remove(token)

        # assigns the rig to the hacker and displays confirmation message
        self.__rig = rig
        print("Rig '" + rig.get_name() + "' has been activated by hacker " + self.__name + ".")

    # Description: Directly assigns a rig to the hacker without spending a CryptoToken.
    # Parameters: rig – The Rig object to be assigned to the hacker.
    # Returns: None
    def assign_rig(self, rig):
        # verifies that the provided object is a Rig
        if isinstance(rig, Rig):
            self.__rig = rig
            # prints a confirmation message showing who received which rig
            print(self.__name, "assigned rig", rig.get_name())

    # Description: Repairs the hacker’s rig using a CryptoToken from inventory.
    # Ensures the hacker has a rig assigned and owns a CryptoToken before performing the repair.
    # This function also Prevents free or invalid repairs by checking conditions first.
    # Parameters: None
    # Returns: None
    def repair_rig(self):
        # checks if the hacker currently has a rig
        if self.__rig is None:
            print(self.__name, "has no rig to repair.")
            return
        # searches the hacker’s inventory for a CryptoToken
        token = None
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == "CryptoToken":
                token = item
        # Checks if the hacker has a CryptoToken before performing a repair.
        if token is None:
            print(self.__name, "has no CryptoToken to repair the rig.")
            return

        # remove the CryptoToken from inventory to simulate it being spent
        self.__inventory.remove(token)
        self.__rig.repair()

    # Description: Launches a Data Spike from the hacker's assigned rig at a target rig.
    # Parameters: target_rig which is The Rig object being attacked.
    # Returns: None
    def launch_data_spike(self, target_rig):
        # blocks action if exposed and prevents further risky actions while the hacker is compromised
        if self.is_exposed():
            print(self.__name, "is exposed and cannot launch attacks until trace is reduced.")
            return

        # ensures the hacker actually has an attacker rig to launch from
        # without a rig there is no source for Data Spike
        if self.__rig is None:
            print(self.__name, "has no rig to launch data spikes.")
            return

        # consume a Data Spike from the attacker's rig storage
        # spikes are a consumable resource; failing here prevents the attack
        if not self.__rig.consume_data_spike():
            print(self.__name, "has no Data Spikes available to launch.")
            return

        # perform the attack: tell the target rig to take a hit
        target_rig.take_hit()

        # increase trace because launching an attack is risky and detectable
        self.__trace_level = self.__trace_level + 1

        # notifies when trace crosses the exposure threshold
        # this informs the player/tests that future actions may be blocked
        if self.__trace_level > 5:
            print(self.__name, "is now EXPOSED! Actions are blocked until trace is reduced.")

        # user-friendly report of attack outcome (broken vs still functional)
        if target_rig.is_broken():
            print(self.__name, "launched Data Spike at", target_rig.get_name(), "— Rig is now broken!")
        else:
            print(self.__name, "launched Data Spike at", target_rig.get_name(), "— Rig is still functional.")

        # if the target broke, attempt extraction by consuming a Removable Drive
        # extraction moves unsecured (unencrypted) assets from the broken rig to hacker inventory
        if target_rig.is_broken():
            if self.__rig.consume_removable_drive():
                unsecured = target_rig.extract_unsecured_assets()
                for asset in unsecured:
                    self.__inventory.append(asset)
                # Prints a message showing how many assets were successfully extracted
                print(self.__name, "extracted", str(len(unsecured)), "unsecured assets from", target_rig.get_name())
            # If there are no removable drives available, extraction cannot happen
            else:
                print(self.__name, "has no removable drive to extract assets from", target_rig.get_name())

    # Description: Encrypts an asset found in the hacker’s inventory or rig storage
    # if not exposed and equipped with a Security Chip.
    # Parameters: asset – the asset object to be encrypted which must exist in inventory or rig storage.
    # Returns: None. Prints messages indicating success or failure of encryption.
    def encrypt_asset(self, asset):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot encrypt assets right now.")
            return
        # Stops if the hacker does not have a Security Chip
        if not self.__has_security_chip:
            print(self.__name, "has no Security Chip to encrypt.")
            return

        found = False  # Tracks if the asset was found and encrypted

        # Searches the hacker's inventory for a matching asset
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == asset.get_name():
                item.encrypt()
                print("Encrypted asset:", str(item))
                found = True

        # If the hacker has a rig, this searches its storage for the asset
        if self.__rig is not None:
            for item in self.__rig.get_storage():
                if check_asset(item) and item.get_name() == asset.get_name():
                    item.encrypt()
                    print("Encrypted asset in rig storage:", item.get_name())
                    found = True

        # If the asset was not found in either inventory or storage this notifies the user
        if not found:
            print("Asset not found in inventory or rig storage; cannot encrypt.")

    # Description: Decrypts an asset found in the hacker’s inventory or rig storage
    # if not exposed and equipped with a Security Chip.
    # Parameters: asset – the asset object to be decrypted which must exist in inventory or rig storage.
    # Returns: None. Prints messages indicating success or failure of decryption.

    def decrypt_asset(self, asset):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot decrypt assets right now.")
            return
        if not self.__has_security_chip:
            print(self.__name, "has no Security Chip to decrypt.")
            return

        found = False  # Tracks if we found the asset

        # Searches inventory by name
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == asset.get_name():
                item.decrypt()
                print("Decrypted asset:", str(item))
                found = True

        # Searches rig storage if hacker has a rig
        if self.__rig is not None:
            for item in self.__rig.get_storage():
                if check_asset(item) and item.get_name() == asset.get_name():
                    item.decrypt()
                    print("Decrypted asset in rig storage:", item.get_name())
                    found = True

        # If not found anywhere, it will print a message and lets the user know.
        if not found:
            print("Asset not found in inventory or rig storage; cannot decrypt.")

    # Description: Upgrades the hacker’s rig by consuming a Hardware Patch asset
    # from inventory if not exposed and a rig is available.
    # Parameters: None. The method automatically searches inventory for a Hardware Patch asset.
    # Returns: None. Prints messages describing success or failure of the rig upgrade.
    def upgrade_rig(self):
        if self.is_exposed():
            print(self.__name, "is exposed and cannot upgrade rigs right now.")
            return
        if self.__rig is None:
            print(self.__name, "has no rig to upgrade.")
            return

        # Finds a Hardware Patch Asset in inventory (searches by name)
        patch = None
        for item in self.__inventory:
            if check_asset(item) and item.get_name() == "Hardware Patch":
                patch = item
        # If no Hardware Patch is found it stops and notifies the user
        if patch is None:
            print("No Hardware Patch found in inventory.")
            return

        # Takes the Hardware Patch out of the hacker’s inventory and applies it to upgrade the rig.
        self.__inventory.remove(patch)
        self.__rig.upgrade()

    # Description: Stores a specific asset from the hacker’s inventory into the assigned rig’s storage if allowed.
    # Parameters: asset – the asset object to be stored and must exist in the hacker’s inventory).
    # Returns: None. Prints messages describing whether storage was successful or why it failed.
    def store_asset(self, asset):
        # Block storing if the hacker is exposed
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
