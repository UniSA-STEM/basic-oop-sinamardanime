"""
File: main.py
Description: <A brief description of this Python module.>
Author: Sina Mardani Mehrabad
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

# Description: Runs a scenario test that simulates a battle using Data Spikes
# and attempts asset extraction from a broken rig.
# Parameters: None.
# Returns: None. Prints setup, storage before/after attack, and a final hacker summary to the console.
def test_battle_and_extraction():
    print("\n--- TEST 1: Battle and Extraction ---")

    # Created rigs for the target and the attacker
    target_rig = Rig("TargetRig")
    attacker_rig = Rig("AttackerRig")

    # Display initial condition and level for the target rig
    print("TargetRig condition / level:", target_rig.get_condition(), "/", target_rig.get_upgrade_level())

    # Created an attacker hacker and assigned the attack rig
    attacker = Hacker("Attacker")
    attacker.assign_rig(attacker_rig)

    # Prepare assets for the target rig: one unencrypted and one encrypted
    secret_doc = Asset("SecretDoc", "Top secret information")
    encrypted_key = Asset("EncryptedKey", "Private key file")
    encrypted_key.encrypt() # marks this asset as encrypted so it should NOT be extracted

    # Adds assets to target rig storage
    target_rig.add_asset(secret_doc)
    target_rig.add_asset(encrypted_key)

    # Displays storage before attack
    print("\nTargetRig storage BEFORE attack:")
    for item in target_rig.get_storage():
        # str(item) prints "[Encrypted]" for encrypted Asset objects
        print("  ", str(item))

    # Launch two data spikes from the attacker to damage / break the target rig
    # Each launch consumes a Data Spike from attacker_rig and increases target rig damage
    attacker.launch_data_spike(target_rig)
    attacker.launch_data_spike(target_rig)


    # This displays stroage after the attack
    # If the rig broke and extraction occurred, the rig's storage will reflect remaining items
    print("\nTargetRig storage AFTER attacks (immediately after break / extraction):")
    for item in target_rig.get_storage():
        print("  ", str(item))

    print("\n--- Hacker Summary ---")
    print(attacker)



# -------------------------------------------------------
# TEST 2 – Encryption and Decryption
# -------------------------------------------------------
# Description: Tests the encryption and decryption process for an asset stored in a hacker’s inventory.
# Parameters: None.
# Returns: None. Prints the results of encryption and decryption actions for verification.
def test_encryption_and_decryption():
    print("\n--- TEST 2: Encryption and Decryption ---")

    # Created a hacker object who will perform encryption/decryption
    hacker = Hacker("Encryptor")

    # Created an asset representing a log file
    file1 = Asset("LogFile", "System activity logs")

    # Added the asset to the hacker's inventory
    hacker.get_inventory().append(file1)

    # Encrypted and then decrypted the same asset to test functionality
    hacker.encrypt_asset(file1)
    hacker.decrypt_asset(file1)


# -------------------------------------------------------
# TEST 3 – Rig Upgrade and Storage
# -------------------------------------------------------
# Description: Tests rig upgrade using a Hardware Patch and verifies storing and retrieving an asset to/from rig storage.
# Parameters: None.
# Returns: None. Shows the setup, actions, and final results on the console.
def test_upgrade_and_storage():
    print("\n--- TEST 3: Rig Upgrade and Storage ---")

    # Created a hacker and rig, then assigned the rig to the hacker
    hacker = Hacker("Upgrader")
    rig = Rig("UpRig")
    hacker.assign_rig(rig)

    # Gave the hacker a Hardware Patch asset that is used to upgrade the rig
    hardware_patch = Asset("Hardware Patch", "Used to upgrade rigs.")
    hacker.get_inventory().append(hardware_patch)

    # Shows rig condition and storage before upgrade
    hacker.upgrade_rig()

    # Created a new asset and test storing it into the rig and retrieving it back
    patch_notes = Asset("PatchNotes", "System update log")
    hacker.get_inventory().append(patch_notes)

    # Stored the asset into the rig which will remove from inventory if successful
    hacker.store_asset(patch_notes)
    print("Rig storage after storing PatchNotes:", [str(i) for i in rig.get_storage()])
    print("Hacker inventory after storing PatchNotes:", [str(i) for i in hacker.get_inventory()])

    # Retrieve the asset back from the rig into inventory
    hacker.retrieve_asset(patch_notes)
    print("Rig storage after retrieving PatchNotes:", [str(i) for i in rig.get_storage()])
    print("Hacker inventory after retrieving PatchNotes:", [str(i) for i in hacker.get_inventory()])


# -------------------------------------------------------
# TEST 4 – Edge Cases
# -------------------------------------------------------

# Description: Tests edge case scenarios to ensure the system handles invalid or special conditions correctly.
# Parameters: None.
# Returns: None. Prints messages showing how each edge case is handled.
def test_edge_cases():
    print("\n--- TEST 4: Edge Cases ---")

    # hacker tries to upgrade without a rig (should fail)
    hacker_no_rig = Hacker("NoRigHacker")
    hacker_no_rig.upgrade_rig()

    # hacker tries to acquire a rig without a CryptoToken
    hacker_no_token = Hacker("BuyerHacker")
    rig = Rig("CheapRig")

    # Removes the CryptoToken from inventory to simulate not having one
    token = None
    for item in hacker_no_token.get_inventory():
        if item.get_name() == "CryptoToken":
            token = item
    if token:
        hacker_no_token.get_inventory().remove(token)
    hacker_no_token.acquire_rig(rig)

    # hacker tries to repair when the hacker has no rig assigned (should print an error)
    hacker_no_repair = Hacker("RepairHacker")
    hacker_no_repair.repair_rig()

    # Assign a rig to the hacker and simulate breaking it
    rig2 = Rig("BrokenRig")
    hacker_no_repair.assign_rig(rig2)

    # Each hit adds damage — after two hits, the rig should be broken
    rig2.take_hit()
    rig2.take_hit()


    # Repair the damaged rig using a CryptoToken (success case)
    hacker_no_repair.repair_rig()

    # Give another CryptoToken to test "no repair needed" scenario
    hacker_no_repair.get_inventory().append(
        Asset("CryptoToken", "Used to acquire or repair rigs.")
    )

    # Try to repair again while rig is pristine (should print "No repair needed")
    hacker_no_repair.repair_rig()

    # Tries to encrypt without a Security Chip (should fail)
    hacker_no_chip = Hacker("NoChipHacker")

    # Disables the hacker’s security chip manually
    hacker_no_chip._Hacker__has_security_chip = False

    # Create a sensitive asset and add it to inventory
    test_asset = Asset("SensitiveFile", "Classified info")
    hacker_no_chip.get_inventory().append(test_asset)
    hacker_no_chip.encrypt_asset(test_asset)
    hacker_no_chip._Hacker__has_security_chip = True




# -------------------------------------------------------
# TEST 5 – Trace Management
# -------------------------------------------------------
# Description: Tests trace behaviour across multiple rig upgrades,
# bulk asset addition, repeated attacks, and encryption blocking when exposed.
# Parameters: None.
# Returns: None. Prints actions
def test_trace_management():
    print("\n--- TEST 5: Trace Management ---")

    # Created a hacker and rig, then assign the rig to the hacker
    hacker = Hacker("Tracer")
    rig = Rig("TraceRig")
    hacker.assign_rig(rig)

    # Give multiple Hardware Patch assets so we can upgrade the rig several times
    hacker.get_inventory().append(Asset("Hardware Patch", "Used to upgrade rigs."))
    hacker.get_inventory().append(Asset("Hardware Patch", "Used to upgrade rigs."))
    hacker.get_inventory().append(Asset("Hardware Patch", "Used to upgrade rigs."))
    hacker.get_inventory().append(Asset("Hardware Patch", "Used to upgrade rigs."))

    # Perform upgrades so each call consumes one Hardware Patch and increases storage capacity
    hacker.upgrade_rig()
    hacker.upgrade_rig()
    hacker.upgrade_rig()
    hacker.upgrade_rig()

    # Attempt to add many Data Spikes to the rig to test the rig's storage limit after upgrades.
    # Count how many Data Spikes were actually accepted (rig.add_asset returns False when storage is full).
    added = 0
    attempts = 40
    for _ in range(attempts):
        ok = rig.add_asset(Asset("Data Spike", "Used in battles."))
        if ok:
            added = added + 1

    print("Attempted to add", attempts, "Data Spikes; actually added", added)

    # Count how many Data Spikes are currently stored in the rig
    # Loops through each item in rig storage and checks if it's an Asset named "Data Spike"
    spikes = 0
    for item in rig.get_storage():
        if isinstance(item, Asset) and item.get_name() == "Data Spike":
            spikes = spikes + 1
    print("Data Spikes available on rig before attacks:", spikes)

    # Launch up to 6 attacks. Each launch consumes a Data Spike from the attacker's rig if they are available
    # and increases the hacker's trace level. I printed the trace after each action to observe the hackers' exposure.
    for i in range(6):
        hacker.launch_data_spike(rig)
        print("Trace Level after action", i + 1, ":", hacker.get_trace_level())

    # Tries encrypting an asset while the hacker may be exposed.
    # Encryption is blocked if trace > exposure threshold or Security Chip missing.
    file1 = Asset("TraceFile", "log data")
    hacker.get_inventory().append(file1)
    print("\nTrying to encrypt asset while EXPOSED:")
    hacker.encrypt_asset(file1)

    # Reduces trace significantly to simulate cooldown and tries encryption again.
    print("\nReducing trace...")
    hacker.reduce_trace(20)
    print("\nTrying again after reducing trace:")
    hacker.encrypt_asset(file1)
    # Attempt another attack which shows the behavior when attempting risky actions after trace changes.
    print("\nAttempting another attack while EXPOSED:")
    hacker.launch_data_spike(rig)

# -----------------------------------------
# TEST 6: Rig Condition Changes
# -----------------------------------------


def test_rig_condition_changes():
    print("\n--- TEST 6: Rig Condition Changes ---")

    rig = Rig("ConditionRig")
    print("Initial condition:", rig.get_condition())

    # Damage test
    rig.take_hit()
    rig.take_hit()
    print("After 2 hits:", rig.get_condition())

    # Repair test
    rig.repair()
    print("After repair:", rig.get_condition())

    # Upgrade test
    rig.upgrade()
    print("After upgrade:", rig.get_condition())

# Description: Runs all test functions in sequence to demonstrate and verify full system behaviour.
# Parameters: None.
# Returns: None. Executes all test cases and prints their results.
def main():
    # Runs test for attacking, breaking rigs, and extracting assets
    test_battle_and_extraction()

    # Runs test for asset encryption and decryption process
    test_encryption_and_decryption()

    # Run test for rig upgrading, storing, and retrieving assets
    test_upgrade_and_storage()


    # Run test for edge cases such as missing rigs, tokens, and chips
    test_edge_cases()

    # Run test for trace level management, upgrades, and exposure logic
    test_trace_management()

    test_rig_condition_changes()


# Description: Ensures that all tests run only when this script is executed directly.

if __name__ == "__main__":
    main()
