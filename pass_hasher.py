from cryptography.fernet import Fernet


def encrypt_pass(password):
    key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
    cipher_suite = Fernet(key)
    ciphered_text = cipher_suite.encrypt(str.encode(password))
    return ciphered_text


def decrypt_pass(password):
    key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
    cipher_suite = Fernet(key)
    unciphered_text = (cipher_suite.decrypt(password))
    return unciphered_text.decode("utf-8")