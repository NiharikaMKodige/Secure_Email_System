import os
import sys

# Add src/ to system path so main.py can import src scripts cleanly
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from key_generator import generate_key_pair
from encrypt_email import encrypt_and_sign
from decrypt_email import decrypt_and_verify

def run_demonstration():
    print("==========================================================")
    print("   BCS703: SECURE EMAIL COMMUNICATION CASE STUDY DEMO     ")
    print("==========================================================\n")

    # Phase 1: Key Generation
    print("--- [PHASE 1] RSA-2048 KEY PAIR GENERATION ---")
    generate_key_pair("alice")
    generate_key_pair("bob")

    # Phase 2: Secure Email Generation (Sender: Alice)
    print("--- [PHASE 2] SENDER SIDE: HYBRID ENCRYPTION & SIGNING ---")
    confidential_message = (
        "Subject: Project Alpha - Security Audit Results\n\n"
        "Dear Bob,\n"
        "The vulnerability assessment is completed. All systems meet IEEE standards.\n"
        "Regards,\nAlice"
    )
    encrypt_and_sign(confidential_message, sender_name="alice", recipient_name="bob")

    # Phase 3: Secure Email Reception (Recipient: Bob)
    print("--- [PHASE 3] RECIPIENT SIDE: DECRYPTION & VERIFICATION ---")
    decrypt_and_verify(sender_name="alice", recipient_name="bob")

if __name__ == "__main__":
    run_demonstration()
    