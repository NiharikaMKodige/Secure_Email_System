import os
import json
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS_DIR = os.path.join(BASE_DIR, "keys")

def load_private_key(person_name: str) -> RSAPrivateKey:
    path = os.path.join(KEYS_DIR, f"{person_name}_private.pem")
    with open(path, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)
        assert isinstance(key, RSAPrivateKey)
        return key

def load_public_key(person_name: str) -> RSAPublicKey:
    path = os.path.join(KEYS_DIR, f"{person_name}_public.pem")
    with open(path, "rb") as f:
        key = serialization.load_pem_public_key(f.read())
        assert isinstance(key, RSAPublicKey)
        return key

def encrypt_and_sign(message_text: str, sender_name: str = "alice", recipient_name: str = "bob"):
    alice_private_key = load_private_key(sender_name)
    bob_public_key = load_public_key(recipient_name)

    message_bytes = message_text.encode('utf-8')

    # 1. Digital Signature: SHA-256 Hash + Alice's Private Key
    signature = alice_private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # 2. Symmetric Encryption: AES-256-GCM
    aes_session_key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(aes_session_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, message_bytes, None)

    # 3. Asymmetric Key Exchange: Encrypt AES Key with Bob's Public Key
    encrypted_session_key = bob_public_key.encrypt(
        aes_session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Package payload formatted as Base64 for easy transport
    payload = {
        "encrypted_session_key": base64.b64encode(encrypted_session_key).decode('utf-8'),
        "nonce": base64.b64encode(nonce).decode('utf-8'),
        "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
        "signature": base64.b64encode(signature).decode('utf-8')
    }

    payload_path = os.path.join(BASE_DIR, "encrypted_payload.json")
    with open(payload_path, "w") as f:
        json.dump(payload, f, indent=4)

    print(f"[SUCCESS] Email encrypted & signed by {sender_name.capitalize()}.")
    print(f"  -> Transmission package saved to: {payload_path}\n")

if __name__ == "__main__":
    print("=== STEP 2: EMAIL ENCRYPTION & SIGNING ===\n")
    sample_email = "Subject: Confidential Security Report\n\nAll cryptographic modules passed validation."
    encrypt_and_sign(sample_email)
    