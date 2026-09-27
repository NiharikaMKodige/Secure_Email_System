import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Path to root project directory (one level up from src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS_DIR = os.path.join(BASE_DIR, "keys")

def generate_key_pair(person_name):
    # 1. Generate RSA-2048 Private Key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # 2. Extract Public Key
    public_key = private_key.public_key()

    # Ensure root 'keys' directory exists
    os.makedirs(KEYS_DIR, exist_ok=True)

    # 3. Save Private Key to PEM file
    private_pem_path = os.path.join(KEYS_DIR, f"{person_name}_private.pem")
    with open(private_pem_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # 4. Save Public Key to PEM file
    public_pem_path = os.path.join(KEYS_DIR, f"{person_name}_public.pem")
    with open(public_pem_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"[SUCCESS] Keys generated for {person_name}:")
    print(f"  - Private Key: {private_pem_path}")
    print(f"  - Public Key : {public_pem_path}\n")

if __name__ == "__main__":
    print("=== STEP 1: RSA KEY GENERATION ===\n")
    generate_key_pair("alice")  # Sender
    generate_key_pair("bob")    # Recipient
    