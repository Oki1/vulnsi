import base64
from hashlib import shake_128

def decrypt_note(encrypted_note, ip_address):
    try:
        key = ip_address.encode()
        decoded = base64.b64decode(encrypted_note)
        decrypted = bytes(x ^ y for x, y in zip(decoded, shake_128(key).digest(len(decoded))))
        # print(decrypted)
        assert decrypted[:128] == bytes(128)
        return decrypted[128:].decode()
    except: return f"[Decryption failed - Invalid key]"

todec = input("todec")

for x in range(2**8):
    for y in range(2**8):
        fk = f"153.5.{x}.{y}"
        # print(fk)
        ret = decrypt_note(todec, fk)
        if(not "[D" in ret):
            print(f"trying {fk}")
            print(ret)
