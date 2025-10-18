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

"""
 Description: Defines the Asset class, representing a digital asset
 that can be encrypted or decrypted, with a name and description.
 Also includes a helper function to verify whether an object is an Asset instance.
 """

class Asset:

    def __init__(self, name, description):
        """
        Description: Initialises a new Asset object.
        Parameters: name – string name of the asset, description – string explanation of its purpose.
        Returns: None
        """
        self.__name = name  #stores asset name
        self.__description = description # stores asset description
        self.__encrypted = False    # ensures asset starts unencrypted



    def encrypt(self):
        """
        Description: Marks this asset as encrypted.
        Encrypted assets are protected and cannot be transferred or extracted until decrypted.
        Parameters: None
        Returns: None
        """
        self.__encrypted = True   # sets encryption flag to True



    def decrypt(self):
        """
        Description: Marks this asset as decrypted (unencrypted).
        Parameters: None
        Returns: None
        """
        self.__encrypted = False # resets encryption flag to False



    def get_name(self):
        """
        Description: Returns the asset’s name.
        Parameters: None
        Returns: str – The name of the asset.
        """
        return self.__name # returns stored asset name



    def set_name(self, new_name):
        """
        Description: Updates the asset’s name.
        Parameters: new_name – The new name for the asset.
        Returns: None
        """
        self.__name = new_name  # updates asset name safely



    def set_description(self, new_description):
        """
        Description: Updates the asset’s description.
        Parameters: new_description – The new description for the asset.
        Returns: None
        """
        self.__description = new_description # updates description safely



    def is_encrypted(self):
        """
        Description: Checks whether the asset is currently encrypted.
        Parameters: None
        Returns: bool – True if encrypted, False otherwise.
        """
        return self.__encrypted # returns encryption status



    def __str__(self):
        """
        Description: Returns a human-readable string showing the asset’s
        name, description, and encryption status.
        Parameters: None
        Returns: str – formatted string representing the asset.
        """
        if self.__encrypted: # checks encryption state before displaying
            return self.__name + ": " + self.__description + " [Encrypted]"
        else:
            return self.__name + ": " + self.__description

def check_asset(obj):
    """
    Description: Helper function that checks if an object is an instance
    of the Asset class. Used throughout the program to safely identify valid asset objects.
    Parameters: obj – The object to test.
    Returns: bool – True if obj is an Asset, False otherwise.
    """
    return isinstance(obj, Asset) # ensures provided object is a valid Asset
