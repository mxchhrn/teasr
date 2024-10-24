import base64
import datetime
import hashlib
import hmac
import json
import os
import random
import re
import shutil
import socket
import string
import struct
import time


# takes given file content and checks if the search string is in the raw input
def search_string_raw(content: bytes, search_str: str) -> bool:
    pattern = search_str.encode()
    if re.findall(pattern, content):
        return True
    return False


# search for patterns in raw input
def search_patterns_raw(raw_bytes: bytes, s_pattern: bytes, e_pattern: bytes) -> list:
    # search for start patterns and save them in matches_start
    start_positions = [m.start() for m in re.finditer(re.escape(s_pattern), raw_bytes)]
    result = []

    # search in raw bytes starting from start matches
    for start in start_positions:
        end_match = re.search(re.escape(e_pattern), raw_bytes[start:])
        if end_match:
            if result:
                if end_match.end() == result[-1][1] - start:
                    continue
            result.append((start, start + end_match.end()))

    return result


# find a key in a dict, or it's sub dicts and outputs the value
def find_key_value(nested_dict, target_key):
    if target_key in nested_dict.keys():
        return nested_dict[target_key]
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            result = find_key_value(value, target_key)
            if result is not None:
                return result
    return None


# return the corresponding hmac
def get_hmac(data: str, key: str) -> str:
    result = hmac.new(key.encode(), data.encode(), digestmod=hashlib.sha256)
    return base64.b64encode(result.digest()).decode()


# outputs the current time as 13 digit timestamp
def get_time_13digit() -> int:
    cur_time = datetime.datetime.now()
    return int(time.mktime(cur_time.timetuple()) * 1000 + cur_time.microsecond/1000)


# get a random string with [a-z0-9] as characters and the given length
def get_random(length: int) -> str:
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for c in range(length))


# prints message on stdout and saves message in log file
def write_message(in_msg: str, log_file: str):
    cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(in_msg)
    with open(log_file, 'a') as f:
        f.write(f"{cur_time}: {in_msg}\n")


# remove all non-printable characters from the input string
def remove_non_printable(in_str: str) -> str:
    return re.sub(r'[\x00-\x1F\x7F]', '', in_str)


# convert an int ip address to the string version
def convert_ip(in_int: int) -> str:
    return socket.inet_ntoa(struct.pack('>i', in_int))


# copy a given file (relative path in app directory) to the output directory
def copy_to_output(app_path: str, out_path: str, log: str, f_name: str) -> str:
    tmp_file = os.path.basename(f_name)
    tmp_path = os.path.join(app_path, f_name)
    write_message(f"Copy file {tmp_file} to {out_path}", log)
    out_file = os.path.join(out_path, tmp_file)
    shutil.copy(tmp_path, out_file)
    return out_file


# write the dictionary to the output file
def write_to_output(in_dict: dict, j_file: str, log_file: str):
    write_message(f"Finished analysis.", log_file)
    write_message(f"Write extracted data to output file...", log_file)
    with open(j_file, 'w') as f:
        json.dump(in_dict, f, indent=2)
    write_message(f"Writing to output file finished.", log_file)
