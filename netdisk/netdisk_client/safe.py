import os
from Crypto.Cipher import AES
from Crypto import Random
import random
import hashlib

# RSA公钥加密
def RSA_enc_pb_key(num, pbkey, n):
    return ((num**pbkey)%n)

# RSA私钥解密
def RSA_dec_pv_key(num, pvkey, n):
    return ((num**pvkey)%n)

# 移位加密
def shift_enc(text, key):
    encrypted = ""
    for char in text:
        if char.isalpha():
            if(ord(char)>96):
                encrypted += chr((ord(char) - ord('a') + key) % 26 + ord('a'))
            else:
                encrypted += chr((ord(char) - ord('A') + key) % 26 + ord('A'))
        else:
            encrypted += char
    return encrypted

# 移位解密
def shift_dec(encrypted, key):
    decrypted = ""
    for char in encrypted:
        if char.isalpha():
            if(ord(char)>96):
                decrypted += chr((ord(char) - ord('a') - key) % 26 + ord('a'))
            else:
                decrypted += chr((ord(char) - ord('A') - key) % 26 + ord('A'))
        else:
            decrypted += char
    return decrypted

# 由私钥生成用于AES加密的64位密钥
def generate_key(pv_key):
    origin = "didongshanyaojlm"
    file_key = ""
    for char in origin:
        file_key += chr((ord(char)-ord("a")+pv_key)%26+ord("a"))
    return file_key    

# 以key为密钥，将source_file_path处的文件加密后保存到destination_file_path处，AES加密形式为CBC
def encrypt_file(key, source_file_path, destination_file_path):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)

    with open(source_file_path, 'rb') as source_file:
        with open(destination_file_path, 'wb') as dest_file:
            dest_file.write(iv)
            while True:
                chunk = source_file.read(1024 * AES.block_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % AES.block_size != 0:
                    chunk += b' ' * (AES.block_size - len(chunk) % AES.block_size)
                dest_file.write(cipher.encrypt(chunk))

# 以key为密钥，将encrypted_file_path处的文件解密后保存到output_file_path处，AES解密形式为CBC                
def decrypt_file(key, encrypted_file_path, output_file_path):
    with open(encrypted_file_path, 'rb') as source_file:
        iv = source_file.read(AES.block_size)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)

        with open(output_file_path, 'wb') as output_file:
            while True:
                chunk = source_file.read(1024 * AES.block_size)
                if len(chunk) == 0:
                    break
                output_file.write(cipher.decrypt(chunk))

# 加密文件：将路径为sp的文件用int密钥加密后放到dp文件夹中，文件名不变                
def enc_file(sp,dp,key):
    file_name = os.path.basename(sp)
    destination_path = dp + file_name
    key = generate_key(key)
    encrypt_file(key, sp, destination_path)
    # print("file encryption complete!")
    return destination_path

# 解密文件：将路径为sp的文件用int密钥解密后放到dp文件夹中，文件名不变
def dec_file(sp,dp,key):
    file_name = os.path.basename(sp)
    destination_path = dp + file_name
    key = generate_key(key)
    decrypt_file(key, sp, destination_path)
    # print("file decryption complete!")
    return destination_path

# 生成一对RSA公私钥，取p=13,q=17
def create_RSA_key_pairs():
    p = 13
    q = 17
    m = (p-1)*(q-1)
    pb_key = random.randint(2,m-1)
    while(gcd(pb_key,m) != 1):
        pb_key = random.randint(2,m-1)
    for pv_key in range(1,m):
        if((pv_key*pb_key)%m == 1):
            break
    return (pb_key,pv_key)

# 计算最大公因数
def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b,a%b)
    
# 用md5函数获取文件哈希值
def calculate_md5(file_path):
   with open(file_path, 'rb') as file:
       md5_hash = hashlib.md5()
       for chunk in iter(lambda: file.read(4096), b""):
           md5_hash.update(chunk)
       return md5_hash.hexdigest()