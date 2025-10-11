# Asset.py
# Represents a digital asset with a name, description, and encryption flag.
# Also provides check_asset(obj) helper to test whether an object is an Asset.



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

    # readable string version of asset (important for printing)
    def __str__(self):
        if self.__encrypted:
            return self.__name + ": " + self.__description + " [Encrypted]"
        else:
            return self.__name + ": " + self.__description

# Helper function: returns True if obj is an Asset instance
def check_asset(obj):
    return isinstance(obj, Asset)
