import base64
from binascii import b2a_hex

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
# from cryptography.hazmat.primitives.asymmetric import rsa

from application.configs import ENCRYPT_KEY
import rsa

from application.constant.util import CommonUtil


def rsa_long_encrypt(pub_key_str, msg, length=100):
    """
    单次加密串的长度最大为 (key_size/8)-11
    1024bit的证书用100， 2048bit的证书用 200
    """
    pubobj = RSA.importKey(pub_key_str)
    pubobj = PKCS1_v1_5.new(pubobj)
    res = []
    for i in range(0, len(msg), length):
        res.append(pubobj.encrypt(msg[i:i + length].encode()))
    return "".join(res)


def rsa_long_decrypt(priv_key_str, msg, length=128):
    """
    1024bit的证书用128，2048bit证书用256位
    """
    privobj = RSA.importKey(priv_key_str)
    privobj = PKCS1_v1_5.new(privobj)
    res = []
    for i in range(0, len(msg), length):
        res.append(base64.b64decode(privobj.decrypt(msg[i:i + length].encode())).decode())
    return "".join(res)


def rsa_encrypt(biz_content, public_key):
    _p = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
    biz_content = biz_content.encode('utf-8')
    # 1024bit key
    default_encrypt_length = 117
    len_content = len(biz_content)
    if len_content <= default_encrypt_length:
        result = b2a_hex(rsa.encrypt(biz_content, _p))
        t = bytes.fromhex(result.decode())
        return base64.b64encode(t).decode()


def rsa_decrypt(biz_content, private_key):
    _pri = rsa.PrivateKey._load_pkcs1_pem(private_key)
    biz_content = base64.b64decode(biz_content.encode())
    # 1024bit key
    default_length = 128
    len_content = len(biz_content)
    if len_content <= default_length:
        return rsa.decrypt(biz_content, _pri).decode()


def rsa_encrypt1(biz_content, public_key):
    _p = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
    biz_content = biz_content.encode('utf-8')
    # 1024bit key
    default_encrypt_length = 117
    len_content = len(biz_content)
    if len_content <= default_encrypt_length:
        return base64.b64encode(b2a_hex(rsa.encrypt(biz_content, _p))).decode()
    offset = 0
    params_lst = []
    while len_content - offset > 0:
        if len_content - offset > default_encrypt_length:
            params_lst.append(b2a_hex(rsa.encrypt(biz_content[offset:offset + default_encrypt_length], _p)).decode())
        else:
            params_lst.append(b2a_hex(rsa.encrypt(biz_content[offset:], _p)).decode())
        offset += default_encrypt_length
    target = ''.join(params_lst)
    return base64.b64encode(target.encode()).decode()


def rsa_decrypt1(biz_content, private_key):
    _pri = rsa.PrivateKey._load_pkcs1_pem(private_key)
    biz_content = base64.b64decode(biz_content)
    # 1024bit key
    default_length = 256
    len_content = len(biz_content)
    if len_content <= default_length:
        return rsa.decrypt(bytes.fromhex(biz_content.decode()), _pri).decode()
    offset = 0
    params_lst = []
    while len_content - offset > 0:
        if len_content - offset > default_length:
            params_lst.append(rsa.decrypt(bytes.fromhex(biz_content[offset: offset + default_length].decode()), _pri).decode())
        else:
            params_lst.append(rsa.decrypt(bytes.fromhex(biz_content[offset:].decode()), _pri).decode())
        offset += default_length
    target = ''.join(params_lst)
    return target


def aes_encrypt():
    # 要加密的明文
    data = {
        'article_id': '24234224dffsdf',
        'tag_id': '2132321'
    }
    data = str(data)
    # 密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.
    # 目前AES-128足够用
    key = '123rwr23sqwe43dr'
    # 生成长度等于AES块大小的不可重复的密钥向量
    iv = Random.new().read(AES.block_size)
    # 使用key和iv初始化AES对象, 使用MODE_CFB模式
    mycipher = AES.new(key, AES.MODE_CFB, iv)
    # 加密的明文长度必须为16的倍数，如果长度不为16的倍数，则需要补足为16的倍数
    # 将iv（密钥向量）加到加密的密文开头，一起传输
    ciphertext = iv + mycipher.encrypt(data.encode())
    # print(b2a_hex(ciphertext).decode())
    return b2a_hex(ciphertext).decode()

def test1():
    key = '123rwr23sqwe43dr'
    data = aes_encrypt()
    params = {
        'key': key,
        'data': data
    }
    params = rsa_encrypt1(str(params), ENCRYPT_KEY.get('public_key'))
    print(params)

    # 解密
    params = CommonUtil.rsa_decrypt(ENCRYPT_KEY.get('private_key'), params)
    print(params)

    key = eval(params).get('key')
    print(key)
    data = eval(params).get('data')
    print(data)

    data = CommonUtil.aes_decrypt(key, data)
    print(data)

    article_id = eval(data).get('article_id')
    tag_id = eval(data).get('tag_id')
    print(article_id)
    print(tag_id)



    # print(CommonUtil.aes_decrypt('123rwr23sqwe43dr',aes_encrypt()))

def test():
    t = open("master-private.pem").read()
    print(type(t))
    recipient_key = RSA.importKey(
        open("master-private.pem").read()
    )
    # print(type(recipient_key))


if __name__ == "__main__":
    msg = "We are different, work hard!We are different, work hard!We are We are different, work hard!We are different, work hard!We are" * 10
    # print(msg)
    #
    # enres = rsa_encrypt1(msg, ENCRYPT_KEY.get('public_key'))
    # print(enres)
    # deres = rsa_decrypt1(enres, ENCRYPT_KEY.get('private_key'))
    # print(deres)
    # str1 = '123'
    # str2 = '234'
    # list1 = []
    # list1.append(base64.b64encode(str1.encode()).decode())
    # list1.append(base64.b64encode(str2.encode()).decode())
    # t = ''.join(list1)
    # aes_encrypt()
    test1()
    # aes_encrypt()
    # print(base64.b64decode(t))
    # print(enres == deres)
