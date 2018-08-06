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
    print(biz_content)
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
            print(rsa.encrypt(biz_content[offset:offset + default_encrypt_length], _p))
            print(b2a_hex(rsa.encrypt(biz_content[offset:offset + default_encrypt_length], _p)).decode())
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
    pad = lambda str: str + (16 - len(str) % 16) * chr(16 - len(str) % 16)
    data = pad(data)
    # print(data)
    # 密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.
    # 目前AES-128足够用
    key = '4McBQHckjLLd1Pzr'
    # 生成长度等于AES块大小的不可重复的密钥向量
    iv = Random.new().read(AES.block_size)
    # print(type(Random.new().read(AES.block_size)))
    # print(iv)
    # 使用key和iv初始化AES对象, 使用MODE_CFB模式
    mycipher = AES.new(key, AES.MODE_CFB, iv)
    # 加密的明文长度必须为16的倍数，如果长度不为16的倍数，则需要补足为16的倍数
    # 将iv（密钥向量）加到加密的密文开头，一起传输
    ciphertext = iv + mycipher.encrypt(data.encode())
    params = mycipher.encrypt(data.encode())
    # print(params)
    # print(b2a_hex(iv).decode() + b2a_hex(mycipher.encrypt(data.encode())).decode())
    # print(b2a_hex(ciphertext).decode())
    return b2a_hex(iv).decode() + b2a_hex(params).decode()

def test2():
    key = 'YzGjs0ovTdDzmZRW'
    data = '3264613339366237616466633433383130165521b4be417c3c9f2accb877d256472646350415a7bb883ec36df505d4bde437781073c93666b52be9198c680fec2515a0e23025d39c925b936e73df9293'
    data = CommonUtil.aes_decrypt(key, data)
    print(data)

def test1():
    key = '4McBQHckjLLd1Pzr'
    data = aes_encrypt()
    # print(data)
    params = {
        'key': key,
        'data': data
    }
    params = rsa_encrypt1(str(params), ENCRYPT_KEY.get('public_key'))
    print(params)

    # 解密
    params = CommonUtil.rsa_decrypt(ENCRYPT_KEY.get('private_key'), params)
    # print(params)

    key = eval(params).get('key')
    # print(key)
    data = eval(params).get('data')
    # print(data)

    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    data = CommonUtil.aes_decrypt(key, data)
    data = unpad(data)
    # print(data)

    article_id = eval(data).get('article_id')
    tag_id = eval(data).get('tag_id')
    # print(article_id)
    # print(tag_id)



    # print(CommonUtil.aes_decrypt('123rwr23sqwe43dr',aes_encrypt()))

def test():
    t = open("master-private.pem").read()
    print(type(t))
    recipient_key = RSA.importKey(
        open("master-private.pem").read()
    )
    # print(type(recipient_key))


def Encrypt(key, iv, instr):
    mystr = _pad(instr)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b2a_hex(iv.encode()).decode() + b2a_hex(cipher.encrypt(mystr)).decode()

def Decrypt(key, encryptedData):
    iv = bytes.fromhex(encryptedData[:32])
    encryptedData = bytes.fromhex(encryptedData[32:])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ret = _unpad(cipher.decrypt(encryptedData))
    ret = ret.decode(encoding="utf-8")
    return ret

def _pad(s):
    BS = AES.block_size
    s = s.encode("utf-8")
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode("utf-8")

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]


if __name__ == "__main__":
    # encryptedData = '346634646135383561376430373132614611aa5d5e03821d6a5e35babd4dc9f72396664aeba8372c9d5220f63f7c57f579e266d38a1f0cf493c5488165264a1c28388b679eb7d317eb5b6554b55f3246'
    # mystr = '合肥'
    # key = 'crL6sStkaN8f43hv'
    # iv = '8765432187654321'
    #
    # # print(Encrypt(key, iv, mystr))
    # print(Decrypt(key, encryptedData))
    test1()

