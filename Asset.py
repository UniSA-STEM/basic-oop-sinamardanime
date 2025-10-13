"""
File: Asset.py
Description: This file defines the Asset class used in the 'Into the Grid' system. It represents digital
items that can be encrypted, decrypted, stored or transferred between hackers and rigs. Each
asset has a name, description and encryption state, and is used in actions such as upgrades,
battles or data protection.

Author: Sina Mardani Mehrabad
ID: Marsyl127
Username: sinamardanime
This is my own work as defined by the University's Academic Misconduct Policy.
"""

# Description: Defines the Asset class, representing a digital asset
# that can be encrypted or decrypted, with a name and description.
# Also includes a helper function to verify whether an object is an Asset instance.
class Asset:
    def __init__(self, name, description):
        # store asset info
        self.__name = name
        self.__description = description
        self.__encrypted = False

    # Description: Marks this asset as encrypted.
    # Encrypted assets are protected and cannot be transferred or extracted until decrypted.
    # Parameters:  None
    # Returns:     None
    def encrypt(self):
        self.__encrypted = True

    # Description: Marks the asset as decrypted (unencrypted).
    # Parameters:  None
    # Returns:     None
    def decrypt(self):
        self.__encrypted = False

    # Description: Returns the asset’s name.
    # Parameters:  None
    # Returns: str – The name of the asset.
    def get_name(self):
        return self.__name

    # Description: Checks whether the asset is currently encrypted.
    # Parameters:  None
    # Returns: a boolean: True if encrypted and False if otherwise.
    def is_encrypted(self):
        return self.__encrypted

    # Description: Returns a human-readable string showing the asset’s name, description, and encryption status.
    # Parameters:  None
    # Returns: A string string (A formatted string representing the asset).
    def __str__(self):
        if self.__encrypted:
            return self.__name + ": " + self.__description + " [Encrypted]"
        else:
            return self.__name + ": " + self.__description

# Description: Helper function that checks if an object is an instance
# of the Asset class. Used throughout the program to safely identify valid asset objects.
# Parameters: obj – The object to test.
# Returns: a boolean: True if obj is an Asset and False if otherwise.
def check_asset(obj):
    return isinstance(obj, Asset)
