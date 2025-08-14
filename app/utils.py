import hashlib, os, hmac

def hash(password: str) -> str:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',           
        password.encode('utf-8'), 
        salt, 
        100_000          
    )
    return salt.hex() + "$" + key.hex()

def verify(plain_password: str, stored: str) -> bool:
    salt_hex, key_hex = stored.split('$')
    salt = bytes.fromhex(salt_hex)
    new_key = hashlib.pbkdf2_hmac(
        'sha256', 
        plain_password.encode('utf-8'), 
        salt, 
        100_000
    )
    return hmac.compare_digest(new_key, bytes.fromhex(key_hex))