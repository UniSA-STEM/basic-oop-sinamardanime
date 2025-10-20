"""
File: Asset.py
Description: This file defines the Asset class used in the 'Into the Grid' system. It represents digital
items that can be encrypted, decrypted, stored or transferred between hackers and rigs. Each
asset has a name, description and encryption state, and is used in actions such as upgrades,
battles or data protection.

Author: Sina Mardani Mehrabad
ID: Marsyl127
Username: sinamardanime
Github repository: https://github.com/UniSA-STEM/basic-oop-sinamardanime.git
This is my own work as defined by the University's Academic Misconduct Policy.
"""

"""
 Description: Defines the Asset class, representing a digital asset
 that can be encrypted or decrypted, with a name and description.
 Also includes a helper function to verify whether an object is an Asset instance.
 """
class Asset:

    """ 
    Description: Initialises a new Asset object.
    Parameters: name - only the string name of the asset, description – string explanation of its purpose.
    Returns: None
    """
    def __init__(self, name, description):
        self.name = name  # stores asset name
        self.__description = description  # stores asset description
        self.__encrypted = False  # ensures asset starts unencrypted



    """ 
    Description: Marks this asset as encrypted.
    Encrypted assets are protected and cannot be transferred or extracted until decrypted.
    Parameters: None
    Returns: None
    """
    def encrypt(self):
        self.__encrypted = True  # sets encryption flag to True



    """ 
    Description: This function marks this asset as decrypted (unencrypted).
    Parameters: None
    Returns: None
    """
    def decrypt(self):
        self.__encrypted = False  # resets encryption flag to False



    """ 
    Description: This function returns the asset’s name.
    Parameters: None
    Returns: str – The name of the asset.
    """
    def get_name(self):
        return self.__name  # returns stored asset name

    """
        Description: This updates the asset’s name with validation using properties to easily retrieve it.
        Parameters: new_name – The new name for the asset.
        Returns: None. Assigns a default name if invalid.
        """

    def set_name(self, new_name):

        # ensures that the provided name is a string
        if isinstance(new_name, str):
            # ensures that it is not blank or only spaces
            if new_name.strip() != "":
                self.__name = new_name  # updates asset name safely
            else:
                print("Error: Asset name cannot be empty. Defaulting to 'Unnamed_Asset'.")
                self.__name = "Unnamed_Asset"
        else:
            print("Error: Invalid asset name type. Expected a string. Defaulting to 'Unnamed_Asset'.")
            self.__name = "Unnamed_Asset"

    name = property(get_name, set_name)  # property linking getter and setter for name

    """ 
    Description: The function updates the asset’s description.
    Parameters: new_description – The new description for the asset.
    Returns: None
    """
    def set_description(self, new_description):
        self.__description = new_description  # updates description safely


    """ 
    Description: Checks whether the asset is currently encrypted.
    Parameters: None
    Returns: bool – True if encrypted, False otherwise.
    """
    def is_encrypted(self):
        return self.__encrypted  # returns encryption status


    """ 
    Description: Returns a human-readable string showing the asset’s
    name, description, and encryption status.
    Parameters: None
    Returns: str – formatted string representing the asset.
    """
    def __str__(self):
        if self.__encrypted:  # checks encryption state before displaying
            return self.__name + ": " + self.__description + " [Encrypted]"
        else:
            return self.__name + ": " + self.__description


""" 
Description: Helper function that checks if an object is an instance
of the Asset class. Used throughout the program to safely identify valid asset objects.
Parameters: obj – The object to test.
Returns: bool – True if obj is an Asset, False otherwise.
"""
def check_asset(obj):
    return isinstance(obj, Asset)  # ensures provided object is a valid Asset
