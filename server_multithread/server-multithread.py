# server_multithread/server.py

import socket
import threading

HOST = '0.0.0.0'
PORT = 8000

def handle_client(conn, addr):
    """
    Função que lida com a comunicação de um único cliente.
    Esta função será executada em uma nova thread.
    """
    print(f"[THREAD] Cliente conectado: {addr}")
    try:
        while True:
            # Recebe dados do cliente
            data = conn.recv(1024)
            if not data:
                print(f"[THREAD] Cliente {addr} desconectado.")
                break
            
            # Devolve a mesma mensagem para o cliente (eco) [cite: 22]
            print(f"[THREAD] Recebido de {addr}: {data.decode('utf-8').strip()}")
            conn.sendall(data)
    except ConnectionResetError:
        print(f"[THREAD] Conexão com {addr} foi resetada.")
    finally:
        conn.close()

def main():
    """
    Função principal que configura o socket e cria uma nova thread para cada cliente.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Vincula o socket à porta especificada 
        server_socket.bind((HOST, PORT))
        server_socket.listen(128)
        print(f"Servidor Multithread escutando em {HOST}:{PORT}")

        while True:
            try:
                # Aceita uma nova conexão [cite: 20]
                conn, addr = server_socket.accept()
                
                # Cria uma nova thread para lidar com o cliente 
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()
                
            except KeyboardInterrupt:
                print("\nServidor Multithread encerrando.")
                break
            except Exception as e:
                print(f"[ERRO] {e}")

if __name__ == "__main__":
    main()