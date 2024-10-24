import shutil
import plyvel
import sqlite3
from . import functions_helper as fhelper


# get the content of a sqlite database as dict
def get_sqlite_db_data(db_path: str) -> dict:
    t_data = {}
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for t in tables:
        cursor.execute(f"SELECT * FROM {t[0]}")
        t_data[t[0]] = cursor.fetchall()
    cursor.close()
    db.close()
    return t_data


# get the content of a LevelDB as dict
def get_leveldb_kv_pairs(db_path: str) -> dict:
    # work on a tmp copy of the given LevelDB (to avoid changing the original data)
    tmp_path = './tmp_leveldb_' + fhelper.get_random(8)
    shutil.copytree(db_path, tmp_path)

    pairs = {}
    db = plyvel.DB(tmp_path, create_if_missing=False)
    for k, v in db:
        tmp_k = k.decode('ascii', errors='ignore')
        tmp_v = v.decode('ascii', errors='ignore')
        pairs[fhelper.remove_non_printable(tmp_k)] = fhelper.remove_non_printable(tmp_v)
    db.close()

    shutil.rmtree(tmp_path)

    return pairs
