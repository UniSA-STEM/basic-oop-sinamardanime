# Asset.py
# Represents a digital asset with a name, description, and encryption flag.
# Also provides check_asset(obj) helper to test whether an object is an Asset.

class Asset:
    def __init__(self, name, description):
        # store asset info
        self.__name = name
        self.__description = description
        # start as unencrypted
        self.__encrypted = False

    # mark asset as encrypted
    def encrypt(self):
        self.__encrypted = True

    # mark asset as decrypted
    def decrypt(self):
        self.__encrypted = False

    # return asset name (used for searching)
    def get_name(self):
        return self.__name

    # check encryption state
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
