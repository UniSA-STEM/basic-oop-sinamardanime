"""
File: main.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""


# -------------------------------------
# Import your three main classes
# -------------------------------------
from Asset import Asset
from Rig import Rig
from Hacker import Hacker


# ----------------------------------------------------------
# Test 1 – Battle and Extraction
# Simulates one hacker attacking another rig and extracting assets
# ----------------------------------------------------------
def test_battle_and_extraction():
    print("\n--- Test 1: Battle and Extraction ---")

    # Target rig setup
    target_rig = Rig("TargetRig")

    # Create two assets for the target rig
    secret_doc = Asset("secret_doc", "top secret information")   # not encrypted
    private_key = Asset("private_key", "encrypted key file")     # encrypted
    private_key.encrypt()

    # Add assets to target rig
    target_rig.add_asset(secret_doc)
    target_rig.add_asset(private_key)

    # Create an attacker hacker and assign them a rig
    attacker_rig = Rig("AttackerRig")
    attacker_hacker = Hacker("Attacker")
    attacker_hacker.assign_rig(attacker_rig)

    # Attacker launches two data spikes (second breaks the target rig)
    attacker_hacker.launch_data_spike(target_rig)
    attacker_hacker.launch_data_spike(target_rig)

    # Show current inventory and target storage contents
    print("\nAttacker's Inventory:")
    for asset in attacker_hacker.get_inventory():
        print(" -", asset)

    print("\nTarget Rig Storage:")
    for asset in target_rig.get_storage():
        print(" -", asset)


# ----------------------------------------------------------
# Test 2 – Encryption and Decryption
# Checks whether encryption and decryption work properly
# ----------------------------------------------------------
def test_encryption_and_decryption():
    print("\n--- Test 2: Encryption and Decryption ---")

    # Create a hacker
    encryption_hacker = Hacker("Encryptor")

    # Add an asset to their inventory
    log_file = Asset("log_file", "temporary logs")
    encryption_hacker.get_inventory().append(log_file)

    # Encrypt and decrypt the asset
    encryption_hacker.encrypt_asset(log_file)
    encryption_hacker.decrypt_asset(log_file)


# ----------------------------------------------------------
# Test 3 – Upgrading and Storage
# Verifies rig upgrades and asset storage/retrieval
# ----------------------------------------------------------
def test_upgrade_and_storage():
    print("\n--- Test 3: Upgrade and Storage ---")

    # Create a hacker and a rig
    upgrade_hacker = Hacker("Upgrader")
    upgrade_rig = Rig("UpRig")
    upgrade_hacker.assign_rig(upgrade_rig)

    # Give hacker a Hardware Patch to perform upgrade
    upgrade_hacker.get_inventory().append("Hardware Patch")
    upgrade_hacker.upgrade_rig()

    # Create a new asset and store/retrieve it
    patch_notes = Asset("patch_notes", "system update logs")
    upgrade_hacker.get_inventory().append(patch_notes)
    upgrade_hacker.store_asset(patch_notes)
    upgrade_hacker.retrieve_asset(patch_notes)


# ----------------------------------------------------------
# Test 4 – Edge Cases
# Tests situations like no rig, no token, and no security chip
# ----------------------------------------------------------
def test_edge_cases():
    print("\n--- Test 4: Edge Cases ---")

    # Case 1: Try upgrading without a rig
    no_rig_hacker = Hacker("NoRigHacker")
    no_rig_hacker.upgrade_rig()   # should print "has no rig to upgrade."

    # Case 2: Try to acquire a rig without CryptoToken
    buyer_hacker = Hacker("BuyerHacker")
    cheap_rig = Rig("CheapRig")
    if "CryptoToken" in buyer_hacker.get_inventory():
        buyer_hacker.get_inventory().remove("CryptoToken")  # remove token
    buyer_hacker.acquire_rig(cheap_rig)  # should print missing token message

    # Case 3: Try to encrypt without Security Chip
    no_chip_hacker = Hacker("NoChipHacker")
    test_file = Asset("test_file", "sensitive data")
    no_chip_hacker.get_inventory().append(test_file)
    no_chip_hacker._Hacker__has_security_chip = False  # temporarily disable chip
    no_chip_hacker.encrypt_asset(test_file)  # should print missing chip message
    no_chip_hacker._Hacker__has_security_chip = True   # restore it


# ----------------------------------------------------------
# Test 5 – Trace Management
# Shows hacker trace increasing and being exposed
# ----------------------------------------------------------
def test_trace_management():
    print("\n--- Test 5: Trace Management ---")

    traced_hacker = Hacker("Tracer")
    traced_rig = Rig("TraceRig")
    traced_hacker.assign_rig(traced_rig)

    # Simulate risky actions that increase trace level
    for i in range(6):  # exceed threshold (for example, 5)
        traced_hacker.launch_data_spike(traced_rig)
        print("Trace Level after action", i + 1, ":", traced_hacker.get_trace_level())


# ----------------------------------------------------------
# MAIN FUNCTION – runs all tests in order
# ----------------------------------------------------------
def main():
    test_battle_and_extraction()
    test_encryption_and_decryption()
    test_upgrade_and_storage()
    test_edge_cases()
    test_trace_management()


# Automatically run main if file is executed directly
if __name__ == "__main__":
    main()