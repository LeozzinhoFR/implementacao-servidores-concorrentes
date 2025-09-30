import asyncio

HOST = '0.0.0.0'
PORT = 8000

async def handle_echo(reader, writer):
    """
    Coroutine que lida com a comunicação de um único cliente.
    O asyncio gerencia a execução concorrente dessas coroutines.
    """
    addr = writer.get_extra_info('peername')
    print(f"[ASYNCIO] Cliente conectado: {addr}")

    try:
        while True:
            # Espera por dados de forma não-bloqueante
            data = await reader.read(1024)
            if not data:
                print(f"[ASYNCIO] Cliente {addr} desconectado.")
                break
            
            message = data.decode('utf-8').strip()
            print(f"[ASYNCIO] Recebido de {addr}: {message}")

            # Envia a resposta de eco [cite: 22]
            writer.write(data)
            # Espera até que o buffer de escrita seja esvaziado
            await writer.drain()

    except asyncio.CancelledError:
        print(f"[ASYNCIO] Conexão com {addr} cancelada.")
    except ConnectionResetError:
        print(f"[ASYNCIO] Conexão com {addr} foi resetada.")
    finally:
        if not writer.is_closing():
            writer.close()
            await writer.wait_closed()

async def main():
    """
    Função principal que inicia o servidor asyncio.
    """
    # Inicia o servidor na porta especificada [cite: 19]
    server = await asyncio.start_server(
        handle_echo, HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Servidor Orientado a Eventos escutando em {addrs}')

    # O servidor roda para sempre até ser interrompido
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor Orientado a Eventos encerrando.")