"""
File: main.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Asset import Asset
from Rig import Rig
from Hacker import Hacker
# -------------------------------------------------------
# TEST 1 – Battle and Extraction
# -------------------------------------------------------
def test_battle_and_extraction():
    print("\n--- TEST 1: Battle and Extraction ---")

    # Create rigs
    target_rig = Rig("TargetRig")
    attacker_rig = Rig("AttackerRig")

    # Create hackers
    attacker = Hacker("Attacker")
    attacker.assign_rig(attacker_rig)

    # Add assets to target rig (1 encrypted, 1 unencrypted)
    secret_doc = Asset("SecretDoc", "Top secret information")
    encrypted_key = Asset("EncryptedKey", "Private key file")
    encrypted_key.encrypt()

    target_rig.add_asset(secret_doc)
    target_rig.add_asset(encrypted_key)

    # Launch two data spikes to break the target rig
    attacker.launch_data_spike(target_rig)
    attacker.launch_data_spike(target_rig)

    # Print final inventories and rig storage
    print("\nAttacker's Inventory:")
    for item in attacker.get_inventory():
        print(" -", item)

    print("\nTarget Rig Storage (remaining):")
    for item in target_rig.get_storage():
        print(" -", item)


# -------------------------------------------------------
# TEST 2 – Encryption and Decryption
# -------------------------------------------------------
def test_encryption_and_decryption():
    print("\n--- TEST 2: Encryption and Decryption ---")

    hacker = Hacker("Encryptor")
    file1 = Asset("LogFile", "System activity logs")

    # Add the asset to inventory
    hacker.get_inventory().append(file1)

    # Encrypt and decrypt the same asset
    hacker.encrypt_asset(file1)
    hacker.decrypt_asset(file1)


# -------------------------------------------------------
# TEST 3 – Rig Upgrade and Storage
# -------------------------------------------------------
def test_upgrade_and_storage():
    print("\n--- TEST 3: Rig Upgrade and Storage ---")

    hacker = Hacker("Upgrader")
    rig = Rig("UpRig")
    hacker.assign_rig(rig)

    # Give hacker a Hardware Patch asset
    hardware_patch = Asset("Hardware Patch", "Used to upgrade rigs.")
    hacker.get_inventory().append(hardware_patch)

    # Upgrade rig
    hacker.upgrade_rig()

    # Add new asset and test storing/retrieving
    patch_notes = Asset("PatchNotes", "System update log")
    hacker.get_inventory().append(patch_notes)
    hacker.store_asset(patch_notes)
    hacker.retrieve_asset(patch_notes)


# -------------------------------------------------------
# TEST 4 – Edge Cases
# -------------------------------------------------------
def test_edge_cases():
    print("\n--- TEST 4: Edge Cases ---")

    # Try to upgrade without a rig
    hacker_no_rig = Hacker("NoRigHacker")
    hacker_no_rig.upgrade_rig()

    # Try to acquire rig without a CryptoToken
    hacker_no_token = Hacker("BuyerHacker")
    rig = Rig("CheapRig")
    # Remove CryptoToken from inventory
    token = None
    for item in hacker_no_token.get_inventory():
        if item.get_name() == "CryptoToken":
            token = item
    if token:
        hacker_no_token.get_inventory().remove(token)
    hacker_no_token.acquire_rig(rig)

    # Try to encrypt without Security Chip
    hacker_no_chip = Hacker("NoChipHacker")
    hacker_no_chip._Hacker__has_security_chip = False  # force off
    test_asset = Asset("SensitiveFile", "Classified info")
    hacker_no_chip.get_inventory().append(test_asset)
    hacker_no_chip.encrypt_asset(test_asset)
    hacker_no_chip._Hacker__has_security_chip = True


# -------------------------------------------------------
# TEST 5 – Trace Management
# -------------------------------------------------------
def test_trace_management():
    print("\n--- TEST 5: Trace Management ---")

    hacker = Hacker("Tracer")
    rig = Rig("TraceRig")
    hacker.assign_rig(rig)

    # Add more Data Spikes so we can do >5 attacks
    for _ in range(8):
        rig.add_asset(Asset("Data Spike", "Used in battles."))

    # Perform multiple attacks
    for i in range(6):
        hacker.launch_data_spike(rig)
        print("Trace Level after action", i + 1, ":", hacker.get_trace_level())

    # Try encrypting while exposed
    file1 = Asset("TraceFile", "log data")
    hacker.get_inventory().append(file1)
    hacker.encrypt_asset(file1)

    # Reduce trace and try again
    hacker.reduce_trace(6)
    hacker.encrypt_asset(file1)


# -------------------------------------------------------
# MAIN DRIVER
# -------------------------------------------------------
def main():
    test_battle_and_extraction()
    test_encryption_and_decryption()
    test_upgrade_and_storage()
    test_edge_cases()
    test_trace_management()









if __name__ == "__main__":
    main()
