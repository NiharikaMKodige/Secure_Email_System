import os
import json
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS_DIR = os.path.join(BASE_DIR, "keys")

def load_private_key(person_name):
    path = os.path.join(KEYS_DIR, f"{person_name}_private.pem")
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(person_name):
    path = os.path.join(KEYS_DIR, f"{person_name}_public.pem")
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def decrypt_and_verify(sender_name="alice", recipient_name="bob"):
    # 1. Load Payload File
    payload_path = os.path.join(BASE_DIR, "encrypted_payload.json")
    if not os.path.exists(payload_path):
        print("[ERROR] Encrypted payload file not found. Run encrypt_email.py first!")
        return

    with open(payload_path, "r") as f:
        payload = json.load(f)

    # Base64 Decode items
    encrypted_session_key = base64.b64decode(payload["encrypted_session_key"])
    nonce = base64.b64decode(payload["nonce"])
    ciphertext = base64.b64decode(payload["ciphertext"])
    signature = base64.b64decode(payload["signature"])

    # 2. Load Recipient's Private Key & Sender's Public Key
    bob_private_key = load_private_key(recipient_name)
    alice_public_key = load_public_key(sender_name)

    # 3. Decrypt AES Session Key using Bob's RSA Private Key
    try:
        aes_session_key = bob_private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"[SUCCESS] {recipient_name.capitalize()} decrypted the AES Session Key.")
    except Exception as e:
        print("[FAIL] Unauthorized Access! Failed to decrypt the AES Session Key.")
        return

    # 4. Decrypt Message using AES-256-GCM Key
    try:
        aesgcm = AESGCM(aes_session_key)
        decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
        decrypted_text = decrypted_bytes.decode('utf-8')
        print(f"[SUCCESS] Email Body Decrypted:\n---\n{decrypted_text}\n---")
    except Exception as e:
        print("[ALERT] Interception / Tampering Detected! Message body corrupted.")
        return

    # 5. Verify Digital Signature using Alice's Public Key
    try:
        alice_public_key.verify(
            signature,
            decrypted_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("\n[VERIFIED] Digital Signature Valid! Message is authentic and from Alice.")
    except Exception as e:
        print("\n[ALERT] Spoofing Warning! Digital Signature verification failed.")

if __name__ == "__main__":
    print("=== STEP 3: EMAIL DECRYPTION & SIGNATURE VERIFICATION ===\n")
    decrypt_and_verify()
    