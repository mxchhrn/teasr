import os
import re
import shutil
from . import functions_os as fos


# run strings on given raw file and save the output
def use_strings(f_path: str, o_path) -> bool:
    cmd = 'strings -t d -n 5 ' + f_path
    err, output = fos.call_subprocess(cmd.split())
    if err:
        return False

    with open(o_path, 'w') as f:
        f.write(output)

    return True


# run bulk_extractor on given raw file and save the outputs in an output path
def use_bulk_extractor(f_path: str, o_path) -> bool:
    cmd = 'bulk_extractor -o ' + o_path + ' ' + f_path
    err, output = fos.call_subprocess(cmd.split())
    if err:
        return False

    # clean up the output directory and delete all empty files
    fos.delete_empty_files(o_path)

    # check if there are output files left
    if len(os.listdir()) < 2:
        print(f"No files found with bulk_extractor for {os.path.basename(f_path)}.")

    return True


# for the fs littlefs extract the files
def use_mklittlefs(p_path: str, o_path: str):
    cmd = 'mklittlefs -u ' + o_path + ' ' + p_path
    err, output = fos.call_subprocess(cmd.split())
    if err:
        return False
    return True


# call bk7231tools dissect_dump to get the decrypted app and bootloader partitions and the kv pairs
def use_bk7231tools(f_path: str, o_path: str) -> bool:
    cmd = 'bk7231tools dissect_dump -e --storage -O ' + o_path + ' ' + f_path
    err, output = fos.call_subprocess(cmd.split())
    if err:
        return False

    list_dir = os.listdir(o_path)

    d_paths = ['encrypt_parts', 'decrypt_parts', 'kv_pairs']

    for i, d in enumerate(d_paths):
        d = os.path.join(o_path, d)
        d_paths[i] = d
        if not os.path.exists(d):
            os.mkdir(d)

    # separate the files in the corresponding directories
    for f in list_dir:
        tmp_f = os.path.join(o_path, f)
        if 'decrypt' in f:
            shutil.move(tmp_f, d_paths[1])
        elif 'storage' in f or 'user_param' in f:
            shutil.move(tmp_f, d_paths[2])
        elif 'app' in f or 'bootloader' in f:
            shutil.move(tmp_f, d_paths[0])

    return True


# save the partition table as dict {ID: [start, length]}
def use_gen_esp32part(img_bytes: bytes) -> tuple[dict, bytes, str]:
    result = {}

    table_start = 4096 * 8
    table_len = 256 * 12
    t_file = 'tmp_file.bin'
    with open(t_file, 'wb') as f:
        f.write(img_bytes[table_start:table_start + table_len])
    cmd = 'gen_esp32part.py ' + t_file
    err, output = fos.call_subprocess(cmd.split())
    if err:
        print(f"Converting the partition table was not possible.")
        exit(1)

    i = 0
    for o in output.split('\n'):
        if '#' not in o:
            tmp = o.split(',')
            # the start is given as hex str -> conv to int
            p_start = int(tmp[3], 16)
            # the length is given as str with unit (i.e. '16K') -> search for digits & conv to int
            p_length = int(re.match(r'\d+', tmp[4]).group()) * 1024
            result[i] = [p_start, p_length]
            i += 1

    return result, img_bytes[table_start:table_start + table_len], output
