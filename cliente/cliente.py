import socket
import sys

def main():
    # Verifica se o host e a porta foram fornecidos como argumentos
    if len(sys.argv) != 3:
        print("Uso: python client.py <host> <porta>")
        sys.exit(1)

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Erro: A porta deve ser um número.")
        sys.exit(1)

    # Cria um socket TCP/IP
    # O 'with' garante que o socket seja fechado automaticamente no final
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Tenta se conectar ao servidor
            print(f"Conectando a {host}:{port}...")
            client_socket.connect((host, port))
            print("Conectado com sucesso ao servidor.")
        except ConnectionRefusedError:
            print(f"Falha na conexão. O servidor em {host}:{port} está ativo?")
            sys.exit(1)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            sys.exit(1)

        print("Digite 'sair' para encerrar a conexão.")

        # Loop principal para enviar e receber mensagens
        while True:
            try:
                # Pede uma mensagem ao usuário
                message = input("> ")
                if message.lower() == 'sair':
                    break

                # Envia a mensagem para o servidor, codificada em bytes
                client_socket.sendall(message.encode('utf-8'))

                # Espera pela resposta do servidor (eco)
                data = client_socket.recv(1024)
                if not data:
                    # Se não receber dados, o servidor fechou a conexão
                    print("\nO servidor encerrou a conexão.")
                    break
                
                # Imprime a resposta recebida, decodificada para string
                print(f"Servidor: {data.decode('utf-8')}")

            except (BrokenPipeError, ConnectionResetError):
                print("\nA conexão com o servidor foi perdida.")
                break
            except KeyboardInterrupt:
                print("\nEncerrando cliente.")
                break

    print("Conexão encerrada.")

if __name__ == "__main__":
    main()