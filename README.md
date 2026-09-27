# Secure Email Communication System 

![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![Cryptography](https://img.shields.io/badge/library-pyca%2Fcryptography-green.svg)

An enterprise-grade hybrid cryptographic email communication model implemented in Python. Designed to protect email messages from **interception**, **spoofing**, and **unauthorized modification**.

---

## 📌 Problem Statement
Traditional email protocols (like plain SMTP) transfer messages across public networks in cleartext. This inherent vulnerability exposes communications to:
1. **Eavesdropping / Interception:** Unencrypted traffic captured by packet sniffers.
2. **Email Spoofing:** Lack of origin authentication allowing identity forgery.
3. **Data Tampering:** Man-in-the-Middle (MitM) alterations during transit.

---

## 🛡️ Key Cryptographic Features & Architecture

This implementation utilizes a **Hybrid Cryptographic Scheme** combining symmetric and asymmetric encryption alongside digital signatures:

* **Confidentiality:** **AES-256-GCM** (Galois/Counter Mode) symmetric encryption ensures payload privacy.
* **Key Exchange:** **RSA-2048 (OAEP Padding)** asymmetric encryption securely wraps session keys.
* **Authenticity & Non-Repudiation:** **RSA-PSS** digital signatures verified via **SHA-256** message digests prove origin.
* **Integrity:** AES-GCM AEAD tags detect any single-bit tampering attempt in transit.

---

## 📁 Repository Structure

```text
Secure_Email_System/
│
├── keys/                           # RSA Public and Private keys (.pem)
├── src/                            # Source modules
│   ├── key_generator.py           # RSA-2048 key pair generation module
│   ├── encrypt_email.py           # Hybrid encryption & digital signature module
│   └── decrypt_email.py           # Decryption & integrity verification module
│
├── main.py                         # End-to-end execution script
├── encrypted_payload.json          # Simulated network transmission payload
├── requirements.txt                # Dependency list
└── README.md                       # Project documentation

```

---

## 🚀 Quick Start Guide

### 1. Prerequisites

Ensure you have **Python 3.12+** installed.

### 2. Installation

Clone this repository and install dependencies:

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/Secure_Email_System.git](https://github.com/YOUR_GITHUB_USERNAME/Secure_Email_System.git)
cd Secure_Email_System
pip install -r requirements.txt

```

### 3. Execution

Run the full demonstration pipeline:

```bash
python main.py

```

Or execute modular steps individually:

```bash
# Step 1: Generate Alice and Bob's RSA key pairs
python src/key_generator.py

# Step 2: Encrypt and digitally sign an email payload
python src/encrypt_email.py

# Step 3: Decrypt the payload and verify signature authenticity
python src/decrypt_email.py

```

---

## 📊 Sample Output

```text
==========================================================
   BCS703: SECURE EMAIL COMMUNICATION CASE STUDY DEMO     
==========================================================

--- [PHASE 1] RSA-2048 KEY PAIR GENERATION ---
[SUCCESS] Keys generated for alice:
  - Private Key: keys/alice_private.pem
  - Public Key : keys/alice_public.pem

[SUCCESS] Keys generated for bob:
  - Private Key: keys/bob_private.pem
  - Public Key : keys/bob_public.pem

--- [PHASE 2] SENDER SIDE: HYBRID ENCRYPTION & SIGNING ---
[SUCCESS] Email encrypted & signed by Alice.
  -> Transmission package saved to: encrypted_payload.json

--- [PHASE 3] RECIPIENT SIDE: DECRYPTION & VERIFICATION ---
[SUCCESS] Bob decrypted the AES Session Key.
[SUCCESS] Email Body Decrypted:
---
Subject: Project Alpha - Security Audit Results

Dear Bob,
The vulnerability assessment is completed. All systems meet IEEE standards.
Regards,
Alice
---

[VERIFIED] Digital Signature Valid! Message is authentic and from Alice.

```

---