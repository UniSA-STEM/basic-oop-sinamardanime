"""
File: main.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""


# Main.py
# Grouped tests covering battles, upgrades, encryption, trace, and edge cases.
# No f-strings used; messages are simple and clear.

from Asset import Asset
from Rig import Rig
from Hacker import Hacker

# ------------------------------
# Test 1 – Battle and Extraction
# ------------------------------
def test_battle_and_extraction():
    print("\n--- Test 1: Battle and Extraction ---")

    # Target rig setup (note: rigs start with two Data Spikes and one Removable Drive)
    target_rig = Rig("TargetRig")

    # Create two assets for the target rig
    secret_doc = Asset("secret_doc", "top secret information")
    private_key = Asset("private_key", "encrypted key file")
    private_key.encrypt()  # keep one encrypted so extraction skips it

    # Add assets to target rig
    target_rig.add_asset(secret_doc)
    target_rig.add_asset(private_key)

    # Attacker setup
    attacker_rig = Rig("AttackerRig")
    attacker_hacker = Hacker("Attacker")
    attacker_hacker.assign_rig(attacker_rig)

    # Attack twice to break target (second hit breaks a level-0 rig)
    attacker_hacker.launch_data_spike(target_rig)
    attacker_hacker.launch_data_spike(target_rig)

    # Print inventory and storage (one per line for readability)
    print("\nAttacker's Inventory:")
    for asset in attacker_hacker.get_inventory():
        print(" -", asset)

    print("\nTarget Rig Storage:")
    for asset in target_rig.get_storage():
        print(" -", asset)


# --------------------------------
# Test 2 – Encryption / Decryption
# --------------------------------
def test_encryption_and_decryption():
    print("\n--- Test 2: Encryption and Decryption ---")

    encryption_hacker = Hacker("Encryptor")
    log_file = Asset("log_file", "temporary logs")
    encryption_hacker.get_inventory().append(log_file)

    encryption_hacker.encrypt_asset(log_file)
    encryption_hacker.decrypt_asset(log_file)


# --------------------------------
# Test 3 – Upgrade and Storage
# --------------------------------
def test_upgrade_and_storage():
    print("\n--- Test 3: Upgrade and Storage ---")

    upgrade_hacker = Hacker("Upgrader")
    upgrade_rig = Rig("UpRig")
    upgrade_hacker.assign_rig(upgrade_rig)

    # give a Hardware Patch and upgrade
    upgrade_hacker.get_inventory().append("Hardware Patch")
    upgrade_hacker.upgrade_rig()

    # store and retrieve one asset
    patch_notes = Asset("patch_notes", "system update logs")
    upgrade_hacker.get_inventory().append(patch_notes)
    upgrade_hacker.store_asset(patch_notes)
    upgrade_hacker.retrieve_asset(patch_notes)


# --------------------------------
# Test 4 – Edge Cases
# --------------------------------
def test_edge_cases():
    print("\n--- Test 4: Edge Cases ---")

    # no rig upgrade attempt
    no_rig_hacker = Hacker("NoRigHacker")
    no_rig_hacker.upgrade_rig()

    # acquire rig without CryptoToken
    buyer_hacker = Hacker("BuyerHacker")
    cheap_rig = Rig("CheapRig")
    if "CryptoToken" in buyer_hacker.get_inventory():
        buyer_hacker.get_inventory().remove("CryptoToken")
    buyer_hacker.acquire_rig(cheap_rig)

    # encrypt without Security Chip
    no_chip_hacker = Hacker("NoChipHacker")
    test_file = Asset("test_file", "sensitive data")
    no_chip_hacker.get_inventory().append(test_file)
    no_chip_hacker._Hacker__has_security_chip = False
    no_chip_hacker.encrypt_asset(test_file)
    no_chip_hacker._Hacker__has_security_chip = True


# --------------------------------
# Test 5 – Trace Management
# --------------------------------
def test_trace_management():
    print("\n--- Test 5: Trace Management ---")

    traced_hacker = Hacker("Tracer")
    traced_rig = Rig("TraceRig")
    traced_hacker.assign_rig(traced_rig)

    # perform six risky actions and print trace level after each
    for i in range(6):
        traced_hacker.launch_data_spike(traced_rig)
        print("Trace Level after action", i + 1, ":", traced_hacker.get_trace_level())


# ------------------------------
# MAIN
# ------------------------------
def main():
    test_battle_and_extraction()
    test_encryption_and_decryption()
    test_upgrade_and_storage()
    test_edge_cases()
    test_trace_management()

if __name__ == "__main__":
    main()
