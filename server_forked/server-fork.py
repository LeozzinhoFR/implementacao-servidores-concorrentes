import os
import socket
import sys

HOST = '0.0.0.0' #Escutar tudo
PORT = 8000

def handle_client(conn, addr): #conn para processo e addr para endereço do cliente
    """
    FUNÇÃO QUE LIDA COM A COMUNICAÇÃO DE UM UNICO CLIENTE, POR ISSO RECEBE APENAS UM ENEDEREÇO
    """
    print(f"[FORKED] Cliente conectado: {addr}")
    try:
        while True:
            # Recebe dados do cliente (até 1024 bytes)
            data = conn.recv(1024)
            if not data:
                # Se não receber dados, o cliente desconectou
                print(f"[FORKED] Cliente {addr} desconectado.")
                break
            
            # Devolve a mesma mensagem para o cliente (eco) [cite: 5]
            print(f"[FORKED] Recebido de {addr}: {data.decode('utf-8').strip()}")
            conn.sendall(data)
    except ConnectionResetError:
        print(f"[FORKED] Conexão com {addr} foi resetada.")
    finally:
        conn.close()
        # É crucial sair do processo filho para não voltar ao loop principal
        sys.exit(0)

def main():
    """
    Função principal que configura o socket e aceita novas conexões.
    """
    # Cria um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Permite reutilizar o endereço para evitar erros de "Address already in use"
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Vincula o socket ao endereço e porta especificados [cite: 19]
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor Forked escutando em {HOST}:{PORT}")

        while True:
            try:
                # Aceita uma nova conexão [cite: 20]
                conn, addr = server_socket.accept()
                
                # Cria um novo processo filho para lidar com o cliente 
                pid = os.fork()
                
                if pid == 0:  # Este é o processo filho
                    server_socket.close()  # O filho não precisa do socket do servidor
                    handle_client(conn, addr)
                else:  # Este é o processo pai
                    conn.close() # O pai não precisa do socket do cliente

            except KeyboardInterrupt:
                print("\nServidor Forked encerrando.")
                break
            except Exception as e:
                print(f"[ERRO] {e}")


if __name__ == "__main__":
    main()