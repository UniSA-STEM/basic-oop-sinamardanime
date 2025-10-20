"""
File: main.py
Description: This program tests the hacker system by creating hackers, rigs and assets.
It runs different parts of the simulation that show how battles, upgrades, encryption and trace
levels work. The tests are grouped into separate sections to clearly show each feature and make
the program easier to check.

Author: Sina Mardani Mehrabad
ID: Marsy127
Username: sinamardanime
Github repository: https://github.com/UniSA-STEM/basic-oop-sinamardanime.git
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Asset import Asset
from Rig import Rig
from Hacker import Hacker
# -------------------------------------------------------
# TEST 1 – Battle and Extraction
# -------------------------------------------------------
"""
Description: Runs a scenario test that simulates a battle using Data Spikes
and attempts asset extraction from a broken rig.
Parameters: None.
Returns: None. Prints setup, storage before/after attack, and a final hacker summary.
"""
def test_battle_and_extraction():
    print("\n--- TEST 1: Battle and Extraction ---")

    # Creates rigs for the target and the attacker
    target_rig = Rig("TargetRig")
    attacker_rig = Rig("AttackerRig")

    # Displays initial condition and level for the target rig
    print("TargetRig condition / level:", target_rig.get_condition(), "/", target_rig.get_upgrade_level())

    # Creates an attacker hacker and assign the rig
    attacker = Hacker("Attacker")
    attacker.assign_rig(attacker_rig)

    print("\n--- Hacker Summary before any attacks ---")
    print(attacker)

    # Prepares assets for target rig
    secret_doc = Asset("SecretDoc", "Top secret information")
    encrypted_key = Asset("EncryptedKey", "Private key file")
    encrypted_key.encrypt()  # marks this asset as encrypted

    # Adds assets to target rig storage
    target_rig.add_asset(secret_doc)
    target_rig.add_asset(encrypted_key)

    # Displays storage before attack
    print("\nTargetRig storage BEFORE attack:")
    for item in target_rig.get_storage():
        print("  ", str(item))

    # Launches two Data Spikes from attacker to break target rig
    attacker.launch_data_spike(target_rig)
    attacker.launch_data_spike(target_rig)

    # Displays storage after attack
    print("\nTargetRig storage AFTER attacks (immediately after break / extraction):")
    for item in target_rig.get_storage():
        print("  ", str(item))

    print("\n--- Hacker Summary ---")
    print(attacker)


# -------------------------------------------------------
# TEST 2 – Encryption and Decryption
# -------------------------------------------------------
"""
Description: Tests encryption and decryption of assets in a hacker’s inventory.
Parameters: None.
Returns: None. Prints results of encryption and decryption for verification.
"""
def test_encryption_and_decryption():
    print("\n--- TEST 2: Encryption and Decryption ---")

    # Creates hacker and asset
    hacker = Hacker("Encryptor")
    file1 = Asset("LogFile", "System activity logs")

    # Adds asset to inventory
    hacker.get_inventory().append(file1)

    # Encrypts and decrypt asset
    hacker.encrypt_asset(file1)
    hacker.decrypt_asset(file1)


# -------------------------------------------------------
# TEST 3 – Rig Upgrade and Storage
# -------------------------------------------------------
"""
Description: Tests rig upgrade using a Hardware Patch and verifies storing/retrieving assets.
Parameters: None.
Returns: None. Displays the sequence of actions and results.
"""
def test_upgrade_and_storage():
    print("\n--- TEST 3: Rig Upgrade and Storage ---")

    # Creates hacker and assign a rig
    hacker = Hacker("Upgrader")
    rig = Rig("UpRig")
    hacker.assign_rig(rig)

    # Gives the hacker a Hardware Patch
    hardware_patch = Asset("Hardware Patch", "Used to upgrade rigs.")
    hacker.get_inventory().append(hardware_patch)

    # Upgrades the rig
    hacker.upgrade_rig()

    # Creates and store a test asset
    patch_notes = Asset("PatchNotes", "System update log")
    hacker.get_inventory().append(patch_notes)
    hacker.store_asset(patch_notes)

    # Shows rig storage and hacker inventory after storing
    print("Rig storage after storing PatchNotes:", [str(i) for i in rig.get_storage()])
    print("Hacker inventory after storing PatchNotes:", [str(i) for i in hacker.get_inventory()])

    # Retrieve the asset back
    hacker.retrieve_asset(patch_notes)
    print("Rig storage after retrieving PatchNotes:", [str(i) for i in rig.get_storage()])
    print("Hacker inventory after retrieving PatchNotes:", [str(i) for i in hacker.get_inventory()])


# -------------------------------------------------------
# TEST 4 – Edge Cases
# -------------------------------------------------------
"""
Description: Tests system behavior in edge scenarios such as missing rigs,
no CryptoTokens, and encryption failures.
Parameters: None.
Returns: None. Prints detailed handling for each edge case.
"""
def test_edge_cases():
    print("\n--- TEST 4: Edge Cases ---")

    # Hacker with no rig tries to upgrade
    hacker_no_rig = Hacker("NoRigHacker")
    hacker_no_rig.upgrade_rig()

    # Hacker with no CryptoToken tries to acquire a rig
    hacker_no_token = Hacker("BuyerHacker")
    rig = Rig("CheapRig")

    # Remove CryptoToken
    token = None
    for item in hacker_no_token.get_inventory():
        if item.get_name() == "CryptoToken":
            token = item
    if token:
        hacker_no_token.get_inventory().remove(token)

    hacker_no_token.acquire_rig(rig)

    # Hacker tries to repair with no rig
    hacker_no_repair = Hacker("RepairHacker")
    hacker_no_repair.repair_rig()

    # Assigns a rig and simulate breaking
    rig2 = Rig("BrokenRig")
    hacker_no_repair.assign_rig(rig2)
    rig2.take_hit()
    rig2.take_hit()

    # Repairs broken rig
    hacker_no_repair.repair_rig()
    print("Hacker inventory after repair:", [str(i) for i in hacker_no_repair.get_inventory()])

    # Tests “no repair needed” condition
    hacker_no_repair.get_inventory().append(Asset("CryptoToken", "Used to acquire or repair rigs."))
    hacker_no_repair.repair_rig()

    # Tests encryption with missing Security Chip
    hacker_no_chip = Hacker("NoChipHacker")
    hacker_no_chip._Hacker__has_security_chip = False
    test_asset = Asset("SensitiveFile", "Classified info")
    hacker_no_chip.get_inventory().append(test_asset)
    hacker_no_chip.encrypt_asset(test_asset)
    hacker_no_chip._Hacker__has_security_chip = True


# -------------------------------------------------------
# TEST 5 – Trace Management
# -------------------------------------------------------
"""
Description: Tests how a hacker’s trace level changes during multiple attacks
and upgrades, including encryption blocking when exposed.
Parameters: None.
Returns: None. Prints trace levels and encryption behavior.
"""
def test_trace_management():
    print("\n--- TEST 5: Trace Management ---")

    hacker = Hacker("Tracer")
    rig = Rig("TraceRig")
    hacker.assign_rig(rig)

    # Adds multiple Hardware Patches
    for _ in range(4):
        hacker.get_inventory().append(Asset("Hardware Patch", "Used to upgrade rigs."))
        hacker.upgrade_rig()

    # Attempts to overfill rig storage with Data Spikes
    added = 0
    attempts = 40
    for _ in range(attempts):
        if rig.add_asset(Asset("Data Spike", "Used in battles.")):
            added += 1
    print("Attempted to add", attempts, "Data Spikes; actually added", added)

    # Launches multiple attacks
    for i in range(6):
        hacker.launch_data_spike(rig)
        print("Trace Level after action", i + 1, ":", hacker.get_trace_level())

    # Tries encryption while exposed
    file1 = Asset("TraceFile", "log data")
    hacker.get_inventory().append(file1)
    print("\nTrying to encrypt asset while EXPOSED:")
    hacker.encrypt_asset(file1)

    # Reduces trace and retry
    print("\nReducing trace...")
    hacker.reduce_trace(20)
    print("\nTrying again after reducing trace:")
    hacker.encrypt_asset(file1)


# -------------------------------------------------------
# TEST 6 – Rig Condition Changes
# -------------------------------------------------------
"""
Description: Tests rig condition changes through hits, repair, and upgrade.
Parameters: None.
Returns: None. Prints changes in condition state.
"""
def test_rig_condition_changes():
    print("\n--- TEST 6: Rig upgrade and damage for a level 0 rig ---")

    rig = Rig("ConditionRig")
    print("Initial condition:", rig.get_condition())

    # Damages twice
    rig.take_hit()
    rig.take_hit()
    print("After 2 hits:", rig.get_condition())

    # Repairs and upgrades
    rig.repair()
    print("After repair:", rig.get_condition())
    rig.upgrade()
    print("After upgrade:", rig.get_condition())


# -------------------------------------------------------
# TEST 7 – Rig Acquisition
# -------------------------------------------------------
"""
Description: Tests if a CryptoToken is consumed when acquiring a rig.
Parameters: None.
Returns: None. Prints inventory before and after acquisition.
"""
def test_rig_acquisition():
    print("\n--- TEST 7: Rig Acquisition ---")

    hacker = Hacker("buyer")
    rig = Rig("NewRig")

    print("Hacker Inventory before acquiring rig:", [str(i) for i in hacker.get_inventory()])
    hacker.acquire_rig(rig)
    print("Inventory after acquiring rig:", [str(i) for i in hacker.get_inventory()])


# -------------------------------------------------------
# TEST 8 – Invalid Name Validation
# -------------------------------------------------------
"""
Description: Tests name validation for Rig, Hacker, and Asset classes
when invalid inputs (e.g., integers or empty strings) are provided. this is to check if the property checks are working.
Parameters: None.
Returns: None. Prints validation messages and resulting names.
"""
def test_invalid_name_validation():
    print("\n--- TEST 8: Invalid Name Validation ---")

    # 1. Invalid name for Rig (integer)
    print("\n[Testing Rig invalid name (integer)]")
    bad_rig = Rig(123)  # should print error and set to 'Unnamed_Rig'
    print("Rig name after validation:", bad_rig.name)

    # 2. Empty string for Rig
    print("\n[Testing Rig empty string name]")
    empty_rig = Rig("")  # should print error and set to 'Unnamed_Rig'
    print("Rig name after validation:", empty_rig.name)

    # 3. Invalid name for Hacker (integer)
    print("\n[Testing Hacker invalid name (integer)]")
    bad_hacker = Hacker(999)  # should print error and set to 'Unknown_Hacker'
    print("Hacker name after validation:", bad_hacker.name)

    # 4. Empty string for Hacker
    print("\n[Testing Hacker empty string name]")
    empty_hacker = Hacker("")  # should print error and set to 'Unknown_Hacker'
    print("Hacker name after validation:", empty_hacker.name)

    # 5. Invalid name for Asset (integer)
    print("\n[Testing Asset invalid name (integer)]")
    bad_asset = Asset(42, "Test asset")
    print("Asset name after validation:", bad_asset.name)

    # 6. Empty string for Asset
    print("\n[Testing Asset empty string name]")
    empty_asset = Asset("", "Empty name test")
    print("Asset name after validation:", empty_asset.name)





# -------------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------------
"""
Description: Runs all test functions in sequence to demonstrate and verify full system behaviour.
Parameters: None.
Returns: None. Executes all test cases and prints their results.
"""
def main():
    test_battle_and_extraction()
    test_encryption_and_decryption()
    test_upgrade_and_storage()
    test_edge_cases()
    test_trace_management()
    test_rig_condition_changes()
    test_rig_acquisition()
    test_invalid_name_validation()

"""
Description: Ensures all tests run only when the script is executed directly.
Parameters: None.
Returns: None.
"""
if __name__ == "__main__":
    main()