#!/usr/bin/env -S PATH="${PATH}:/opt/homebrew/bin:/usr/local/bin" python3

# World Clock plugin
#
# by ansidev (ansidev@gmail.com)
#
# metadata
# <xbar.title>World Clock plugin</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Le Minh Tri</xbar.author>
# <xbar.author.github>ansidev</xbar.author.github>
# <xbar.desc>World Clock plugin</xbar.desc>

import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime

# Timezones
timezones = [
    "Asia/Ho_Chi_Minh",
    "Australia/Canberra",
    "Asia/Seoul",
]
time_format= "%a %d %b %H:%M"

script_file_path = os.path.abspath(sys.argv[0])
script_file_name = os.path.basename(sys.argv[0])
script_name, _ = os.path.splitext(script_file_name)

config_file_path = f"configs/{script_name}.cfg"

# functions
def write_to_file(file_path, file_content):
    with open(file_path, "w") as file:
        file.write(file_content)

def get_formatted_text(timezone_name):
    try:
        timezone = pytz.timezone(timezone_name)
        current_time = datetime.now(timezone)
        formatted_time = current_time.strftime(time_format)
        city_name = get_city_name(timezone_name)
        return f"{formatted_time} {city_name}"
    except pytz.UnknownTimeZoneError:
        return get_formatted_text(timezones[0])

def get_city_name(timezone_name):
    parts = timezone_name.split('/')
    if len(parts) < 2:
        return ""
    return re.sub(r'_', ' ', parts[1], flags=re.IGNORECASE)

'''Display instructions if the dependencies are not installed'''
try:
    import pytz
except:
    print(":warning: World Clock")
    print("---")
    print("Please install the dependencies by clicking below | color=black")
    print("Install dependencies | color=green bash='pip3 install pytz' refresh=true")
    print("---")
    sys.exit(1)

# Create config directory if it does not exists
config_dir_path = os.path.dirname(config_file_path)
if not os.path.exists(config_dir_path):
    os.makedirs(config_dir_path)

# Get the current profile
try:
    with open(config_file_path, "r") as file:
        current_timezone = file.read().strip()
except FileNotFoundError:
    current_timezone = timezones[0]
    write_to_file(config_file_path, current_timezone)

# Render menu
current_text = get_formatted_text(current_timezone)
print(f"{current_text}")
print("---")
for tz in timezones:
    tz_text = get_formatted_text(tz)
    menu_item_text = f"✓ {tz_text}" if tz == current_timezone else f"⠀ {tz_text}"
    print(f"{menu_item_text} | shell='{script_file_path}' param1='{tz}' terminal=false refresh=true")

# Handle command-line arguments
if len(sys.argv) == 2:
    selected_timezone = sys.argv[1]
    write_to_file(config_file_path, selected_timezone)
