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

# Target rig setup
target = Rig("TargetRig")
a1 = Asset("secret_doc", "top secret")
a2 = Asset("private_key", "encrypted key")
a2.encrypt()
target.add_asset(a1)
target.add_asset(a2)

# Attacker setup
attacker_rig = Rig("AttackerRig")
attacker = Hacker("Attacker")
attacker.assign_rig(attacker_rig)

# Attack sequence
attacker.launch_data_spike(target)
attacker.launch_data_spike(target)

# Results after extraction
print("Attacker inventory:", [str(x) for x in attacker.get_inventory()])
print("Target storage:", [str(x) for x in target.get_storage()])

# Encryption test
extra_asset = Asset("log_file", "temporary logs")
attacker.get_inventory().append(extra_asset)
attacker.encrypt_asset(extra_asset)
attacker.decrypt_asset(extra_asset)
attacker_rig.add_asset(extra_asset)
attacker.encrypt_asset(extra_asset)

# Upgrade test
attacker.get_inventory().append("Hardware Patch")
attacker.upgrade_rig()

# Store and retrieve test
asset2 = Asset("notes", "simple text")
attacker.get_inventory().append(asset2)
attacker.store_asset(asset2)
attacker.retrieve_asset(asset2)

# Scan test
attacker.scan_inventory("notes")
