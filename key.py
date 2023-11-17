from cryptography.fernet import Fernet

# Hardcoded key value
key_value = "PjAJj1Scb0ywqwI6tG3SuaPg54A0FulRKyvp_F__kO8="
key_value = key_value.encode()


def get_fernet_instance():
    # Instance the Fernet class with the key
    return Fernet(key_value)
