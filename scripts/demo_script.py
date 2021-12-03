"""
"""
import json
import time

from scripts.set_up_enviroment import *


def run_script():
    base_url_valid_validator = "http://localhost:8005"
    base_url_cheater = "http://localhost:8006"
    print("Setting up environment ....")
    ###setup environment prepare for submit grades

    setup_environment(base_url_valid_validator)
    print("Run script demo for invalid editing grades")
    # 1. Submit grades
    msg, status = submit_grate(base_url_valid_validator)
    pretty_msg = json.dumps(msg, indent=4, sort_keys=True)
    print(f"""
1. Submit grades
{pretty_msg}
    """)
    time.sleep(3)

    msg, status = get_grade_in_script()
    pretty_msg = json.dumps(msg, indent=4, sort_keys=True)
    print(f"""
Current grade
{pretty_msg}
    """)

    # 2. Edit grades
    msg, status = edit_grade(base_url_valid_validator)
    pretty_msg = json.dumps(msg, indent=4, sort_keys=True)
    print(f"""
2. Edit grades  
{pretty_msg}
    """)
    time.sleep(3)
    msg, status = get_grade_in_script()
    pretty_msg = json.dumps(msg, indent=4, sort_keys=True)
    print(f"""
Grade after edit
{pretty_msg}
    """)
    # 3. Invalid edit grades
    msg, status = invalid_edit_grade(base_url_cheater)
    pretty_msg = json.dumps(msg, indent=4, sort_keys=True)
    print(f"""
3. Invalid edit grades  
{pretty_msg}    
    """)
    msg, status = get_grade_in_script()
    pretty_msg = json.dumps(msg, indent=4, sort_keys=True)
    print(f"""
Grade after invalid edit
{pretty_msg}
    """)


run_script()
