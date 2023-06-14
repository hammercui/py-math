import hashlib
import re
import socket
import string
import uuid


class Tools:
    def __init__(self):
        print(f"Utils >>>\t initiated")

    @staticmethod
    def gen_uuid():
        """ 生成UUID """
        uid = uuid.uuid1()
        return uid.hex

    @staticmethod
    def get_host_ip():
        """ 获取当前设备局域网 ip 地址 """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    @staticmethod
    def remove_punct(text):
        """
        正则去掉字符串中所有的标点符号
        :param text: 带标点的字符串
        :return: 不带标点的字符串
        """
        res_str = text.translate(str.maketrans('', '', string.punctuation))
        return res_str

    @staticmethod
    def format_address(contract):
        """ 格式化合约地址 """
        if not contract.startswith('0x'):
            contract = f"0x{contract}"
        return str(contract).lower()

    @staticmethod
    def filter_emoji(desstr, restr=''):
        """ 过滤表情 """
        if desstr is None or desstr == 'None':
            return ''
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub(restr, desstr)

    @staticmethod
    def get_sha1(content):
        hash_sha1 = hashlib.sha1(str(content).encode("utf-8")).hexdigest()
        return hash_sha1

    @staticmethod
    def get_bucket(content, bucket_size=1000):
        hash_sha1 = Tools.get_sha1(content)
        bucket_id = int(hash_sha1, 16) % bucket_size
        return bucket_id

    @staticmethod
    def kwargs2url(base_url, **kwargs):
        base = base_url
        is_first = True
        for key, value in list(kwargs.items()):
            if value is None:
                continue

            if is_first:
                base += f"{key}={value}"
                is_first = False
            else:
                base += f"&{key}={value}"
        return base

    @staticmethod
    def isNone(value):
        return value is None or value == 'None'

    @staticmethod
    def isNotNone(value):
        return value is not None and value != 'None'
