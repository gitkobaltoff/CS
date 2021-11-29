from base64 import b64decode
import os

from pymongo import MongoClient
from pymongo.encryption_options import AutoEncryptionOpts
from bson.binary import Binary, UUID_SUBTYPE
import bson.json_util

if "LOCAL_MASTER_KEY" not in os.environ or not os.path.exists(
        "key_uuid.txt"):
    raise Exception("Prerequisites not met. Run create_key.py")

master_key = Binary(b64decode(os.environ["LOCAL_MASTER_KEY"]))
key_uuid = Binary(b64decode(open("key_uuid.txt", "r").read()), UUID_SUBTYPE)

# Reset collection
MongoClient().lab7.data.drop()


def dumps(doc):
    return bson.json_util.dumps(doc, indent=4)


# Automatic encryption and decryption
# Requires MongoDB enterprise
kms_providers = {"local": {"key": master_key}}
schema_map = {
    "lab7.data": {
        "bsonType": "object",
        "properties": {
            "ssn": {
                "encrypt": {
                    "bsonType": "string",
                    "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
                    "keyId": [key_uuid]
                }
            },
        }
    }
}

encryption_opts = AutoEncryptionOpts(
    kms_providers,
    "lab7.key_vault",
    schema_map=schema_map,
    mongocryptd_bypass_spawn=True)

encrypted_data = MongoClient(auto_encryption_opts=encryption_opts).lab7.data
unencrypted_data = MongoClient().lab7.data

encrypted_data.insert_one({"name": "Doris", "surname": "Jones", "ssn": "457-55-5462"})
encrypted_data.insert_one({"name": "Ellis", "surname": "Smith", "ssn": "234-45-1111"})

print("Print without auto decryption:")
print(dumps(unencrypted_data.find({}, {"_id": 0, "name": 1, "surname": 1, "ssn": 1})))

print("Print with auto decryption:")
print(dumps(encrypted_data.find({}, {"_id": 0, "name": 1, "surname": 1, "ssn": 1})))
