#!/usr/bin/env -S PATH="${PATH}:/opt/homebrew/bin:/usr/local/bin" python3

# Key Binding plugin
#
# by ansidev (ansidev@gmail.com)
#
# metadata
# <xbar.title>Key binding plugin</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Le Minh Tri</xbar.author>
# <xbar.author.github>ansidev</xbar.author.github>
# <xbar.desc>Key binding plugin</xbar.desc>

import os
import subprocess
import sys
import tempfile

# Key binding profiles
profiles = {
    "default": {
        "name": "Default",
        "mapping": '[]'
    },
    "akko_3098n": {
        "name": "AKKO 3098N",
        "mapping": '[{"HIDKeyboardModifierMappingSrc":0x7000000E3,"HIDKeyboardModifierMappingDst":0x7000000E2},{"HIDKeyboardModifierMappingSrc":0x7000000E0,"HIDKeyboardModifierMappingDst":0x7000000E3},{"HIDKeyboardModifierMappingSrc":0x7000000E2,"HIDKeyboardModifierMappingDst":0x7000000E0},{"HIDKeyboardModifierMappingSrc":0x70000004B,"HIDKeyboardModifierMappingDst":0x70000004A},{"HIDKeyboardModifierMappingSrc":0x70000004E,"HIDKeyboardModifierMappingDst":0x70000004D}]'
    },
    "semico": {
        "name": "SEMICO",
        "mapping": '[{"HIDKeyboardModifierMappingSrc":0x7000000E3,"HIDKeyboardModifierMappingDst":0x7000000E0},{"HIDKeyboardModifierMappingSrc":0x7000000E0,"HIDKeyboardModifierMappingDst":0x7000000E3}]'
    },
}

script_file_path = os.path.abspath(sys.argv[0])
script_file_name = os.path.basename(sys.argv[0])
script_name, _ = os.path.splitext(script_file_name)

config_file_path = f"configs/{script_name}.cfg"

# functions
def write_to_file(file_path, file_content):
    with open(file_path, "w") as file:
        file.write(file_content)

def activate_profile(profile_id):
    mapping = profiles[profile_id]['mapping']
    mapping_str = '{"UserKeyMapping": ' + mapping + '}'
    command_args = ["hidutil", "property", "--set", mapping_str]
    subprocess.run(command_args)

# Create config directory if it does not exists
config_dir_path = os.path.dirname(config_file_path)
if not os.path.exists(config_dir_path):
    os.makedirs(config_dir_path)

# Get the current profile
try:
    with open(config_file_path, "r") as file:
        current_profile_id = file.read().strip()
except FileNotFoundError:
    current_profile_id = "default"
    write_to_file(config_file_path, current_profile_id)

# activate_profile(current_profile_id)

# Render menu
current_profile_name = profiles[current_profile_id]['name']
print(f"{current_profile_name}")
print("---")
for profile_id, profile in profiles.items():
    profile_name = f"✓ {profile['name']}" if profile_id == current_profile_id else f"⠀ {profile['name']}"
    print(f"{profile_name} | shell='{script_file_path}' param1='{profile_id}' terminal=false refresh=true")

# Handle command-line arguments
if len(sys.argv) == 2:
    selected_profile = sys.argv[1]
    write_to_file(config_file_path, selected_profile)
    print(f"Select profile: {selected_profile}")
    activate_profile(selected_profile)
