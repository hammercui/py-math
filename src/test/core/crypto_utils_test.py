from core.logger_class import Logger
from core.config_class import LoadConfig
from core.crypto_class import Crypto

logger = Logger()
logger.init(env="dev")
config = LoadConfig()
config.init(env="dev")
crypto = Crypto()

if __name__ == "__main__":
    msg = "hello 123!"
    logger.info(f"origin  data:\t{msg}")

    # ********************************* Base64 *********************************
    msg_e = crypto.str2base64(msg)
    logger.info(f"str2base64:\t{msg_e}")

    msg_e = 'data:application/json;base64,eyJuYW1lIjogIlpvcmEgQVBJIEdlbmVzaXMgSGFja2F0aG9uIDg3MzEyIiwgImRlc2NyaXB0aW9uIjogIkluIEp1bmUgb2YgMjAyMiBidWlsZGVycyBmcm9tIGFjcm9zcyB0aGUgaW50ZXJuZXQgY2FtZSB0b2dldGhlciB0byBoYWNrIG9uIHRvcCBvZiB0aGUgWm9yYSBBUEkgYW5kIHByb2R1Y2UgY3JlYXRpb25zIHNob3djYXNpbmcgdGhlIHBvd2VyIG9mIE5GVHMuIiwgImltYWdlIjogImlwZnM6Ly9iYWZrcmVpZ3lxNnQ0cmFvY2tmN21ma2JtanV4d2IzY3lmcGpnY3g0dnNxdHZ1NmRnbmk3ZjN3Y2dsND9pZD04NzMxMiIsICJhbmltYXRpb25fdXJsIjogImlwZnM6Ly9iYWZ5YmVpZzR4ZHhhYWxzN2VoaHhwa2djam14MjRiNWdrYWY2bGYydG5wbnBrcHpla2p4YnkyZ2hzbT9pZD04NzMxMiIsICJwcm9wZXJ0aWVzIjogeyJudW1iZXIiOiA4NzMxMiwgIm5hbWUiOiAiWm9yYSBBUEkgR2VuZXNpcyBIYWNrYXRob24ifX0='
    msg_d = crypto.base642str(msg_e.split(',')[-1])
    logger.info(f"base642str:\t{msg_d}\n")

    # ******************************* 对称加密 AES 测试 ********************************
    key, iv = crypto.generate_aes_keypair()
    logger.info(f"AES Key Pair:\naes key:\n{key}\naes  iv:\n{iv}")

    msg_e = crypto.encrypt_aes(msg)
    logger.info(f"aes encrypt data:\t{msg_e}")

    msg_d = crypto.decrypt_aes(msg_e)
    logger.info(f"aes decrypt data:\t{msg_d}\n")

    # ******************************* 非对称加密 RSA 测试 ********************************
    public_pem, private_pem = crypto.generate_rsa_keypair()
    logger.info(f"RSA Key Pair:\nrsa public key:\n{public_pem}\nrsa private key:\n{private_pem}")

    msg_e = crypto.encrypt_rsa(msg)
    logger.info(f"rsa encrypt data:\t{msg_e}")

    msg_d = crypto.decrypt_rsa(msg_e)
    logger.info(f"rsa decrypt data:\t{msg_d}")
