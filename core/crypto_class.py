import sys
import os
import base64
import random
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

# cur_abs_path = os.path.dirname(os.path.abspath(__file__))
# if cur_abs_path not in sys.path:
#     sys.path.append(cur_abs_path)
from core.config_class import LoadConfig
from core.singleton_class import Singleton


class Crypto(Singleton):
    def __init__(self):
        self.config = LoadConfig.instance()
        self.aes_key = self.config.get("SECURITY_CRY_KEY")
        self.aes_iv = self.config.get("SECURITY_CRY_IV")
        self.rsa_public_key = self.config.get("SECURITY_RSA_PUBLIC_KEY")
        self.rsa_private_key = self.config.get("SECURITY_RSA_PRIVATE_KEY")
        print(f"Crypto >>>\t initiated")

    @staticmethod
    def instance():
        return Crypto()

    @staticmethod
    def generate_aes_keypair():
        """生成随机 AES IV"""
        key_array = random.sample("abcdefghijklmnopqrstuvwxyz!@#$%^&*()", 16)
        iv_array = random.sample("abcdefghijklmnopqrstuvwxyz!@#$%^&*()", 16)
        key = ""
        iv = ""
        for i in range(0, 16):
            key += key_array[i]
            iv += iv_array[i]
        return key, iv

    def encrypt_aes(self, text: str):
        """
        AES.MODE_CBC 加密 CBC模式
        密钥（key）, 密斯偏移量（iv）
        """
        key = bytes(self.aes_key, encoding="utf-8")
        iv = bytes(self.aes_iv, encoding="utf8")
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        text = pad(text)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypt_bytes = cipher.encrypt(text.encode("utf8"))  # 加密后得到的是bytes类型的数据
        encrypt_text = str(base64.b64encode(encrypt_bytes), encoding="utf-8")  # 使用Base64进行编码,返回byte字符串, 再转为 utf-8 字符串
        return encrypt_text

    def decrypt_aes(self, text_encrypted_base64: str, p_key=None, p_iv=None):
        """
        AES.MODE_CBC 解密 CBC模式
        密钥（key）, 密斯偏移量（iv）
        """
        key = bytes(p_key, encoding="utf-8") if p_key is not None else bytes(self.aes_key, encoding="utf-8")
        iv = bytes(p_iv, encoding="utf8") if p_iv is not None else bytes(self.aes_iv, encoding="utf8")

        cipher = AES.new(key, AES.MODE_CBC, iv)
        text_encrypted_base64 = base64.b64decode(text_encrypted_base64)

        text_decrypted = cipher.decrypt(text_encrypted_base64)
        unpad = lambda s: s[0: -s[-1]]
        text_decrypted = unpad(text_decrypted)

        return text_decrypted.decode("utf8")

    @staticmethod
    def generate_rsa_keypair():
        """ 生成 RSA 公钥和私钥 """
        random_generator = Random.new().read
        rsa = RSA.generate(1024, random_generator)

        private_pem = str(base64.b64encode(rsa.exportKey()), 'utf-8')
        public_pem = str(base64.b64encode(rsa.publickey().exportKey()), 'utf-8')
        return public_pem, private_pem

    def encrypt_rsa(self, text: str):
        """ rsa 加密 """
        public_key_bytes = base64.b64decode(self.rsa_public_key)
        # 字符串指定编码（转为bytes）
        text = text.encode('utf-8')
        # 构建公钥对象
        cipher_public = PKCS1_v1_5.new(RSA.importKey(public_key_bytes))
        # 加密（bytes）
        text_encrypted = cipher_public.encrypt(text)
        # base64编码，并转为字符串
        text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
        return text_encrypted_base64

    def decrypt_rsa(self, text_encrypted_base64: str):
        """ rsa 解密 """
        private_key_bytes = base64.b64decode(self.rsa_private_key)
        # 字符串指定编码（转为bytes）
        text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
        # base64解码
        text_encrypted = base64.b64decode(text_encrypted_base64)
        # 构建私钥对象
        cipher_private = PKCS1_v1_5.new(RSA.importKey(private_key_bytes))
        # 解密（bytes）
        text_decrypted = cipher_private.decrypt(text_encrypted, Random.new().read)
        # 解码为字符串
        text_decrypted = text_decrypted.decode()
        return text_decrypted

    @staticmethod
    def str2base64(str_msg):
        str_byte = str_msg.encode('utf-8')
        str_base64 = str(base64.b64encode(str_byte), 'utf-8')
        return str_base64

    @staticmethod
    def base642str(str_base64):
        str_byte = base64.b64decode(
            str_base64 + '==')  # https://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding
        str_msg = str_byte.decode('utf-8')
        return str_msg
