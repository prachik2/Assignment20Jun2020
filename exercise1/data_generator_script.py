import string
import random
import uuid
import MySQLdb
import struct
import socket

from datetime import datetime
from exercise1.exercise1.settings import DATABASES

now = datetime.now()
dbconn = MySQLdb.connect(
    database=DATABASES["default"]["NAME"], user=DATABASES["default"]["USER"], password=DATABASES["default"]["PASSWORD"], host=DATABASES["default"]["HOST"])


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def unique_mac_address(n_unique,
                       pool: str = string.ascii_letters) -> set:
    """Generate a set of unique string tokens.

    k: Length of mac_address token
    ntokens: Number of tokens
    pool: Iterable of characters to choose from

    For a highly optimized version:
    """
    seen = set()
    length_of_mac_address = 12
    # An optimization for tightly-bound loops:
    # Bind these methods outside of a loop
    join = ''.join
    add = seen.add

    while len(seen) < n_unique:
        split_strings = []
        n = 2
        token = join(random.choices(pool, k=length_of_mac_address))
        for index in range(0, len(token), n):
            split_strings.append(token[index: index + n])

        mac_address_token = ":".join(split_strings)

        add(mac_address_token)
    return seen


def random_sap_id(n_unique):
    sap_ids = []
    for i in range(0, n_unique):
        range_start = 10 ** (17 - 1)
        range_end = (10 ** 17) - 1
        sap_ids.append("S" + str(random.randint(range_start, range_end)))
    return sap_ids


def insert_data():
    mac_address = list(unique_mac_address(n_unique))
    sap_ids = random_sap_id(n_unique)
    for i in range(len(mac_address)):
        with dbconn.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("insert ignore into network_details(id,creator_id,updater_id,is_deleted,date_updated,date_added,\
                                                                                    auto_id,sap_id,loop_back,host_name,mac_address)\
                                                                                    values (%s,%s,%s,%s,%s,%s,\
                                                                                    %s,%s,%s,%s,%s) ;",
                           (
                           [uuid.uuid1(), 1, 1, 0, now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S"),
                            i, sap_ids[i], socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))), socket.inet_ntoa(struct.pack('<I',random.randint(1, 0xffffffff))),mac_address[i]]))
            dbconn.commit()


if __name__ == "__main__":
    n_unique = int(input("Enter No. of records to be inserted:(1...n)"))
    insert_data()
    print(insert_data(), "Inserted.")
