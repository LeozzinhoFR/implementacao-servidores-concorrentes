# client/load_tester.py
import asyncio
import sys
import time

async def create_client(host, port, num_messages, client_id):
    """Uma coroutine que simula um único cliente."""
    try:
        reader, writer = await asyncio.open_connection(host, port)
        
        message = f"Hello from client {client_id}"
        encoded_message = message.encode()
        
        for i in range(num_messages):
            writer.write(encoded_message)
            await writer.drain()
            
            data = await reader.read(1024)
            if not data:
                return 0 # Conexão fechada pelo servidor

        writer.close()
        await writer.wait_closed()
        return num_messages # Sucesso
        
    except (ConnectionRefusedError, OSError):
        return 0 # Falha na conexão
    except Exception as e:
        # print(f"Erro no cliente {client_id}: {e}")
        return 0

async def main():
    if len(sys.argv) != 5:
        print("Uso: python load_tester.py <host> <porta> <num_clientes> <msgs_por_cliente>")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    num_clients = int(sys.argv[3])
    msgs_per_client = int(sys.argv[4])

    print(f"Iniciando teste de carga em {host}:{port}...")
    print(f"Clientes: {num_clients}, Mensagens por cliente: {msgs_per_client}")
    
    start_time = time.perf_counter()
    
    # Cria e agenda todas as tarefas de cliente
    tasks = [create_client(host, port, msgs_per_client, i) for i in range(num_clients)]
    
    # Espera que todas as tarefas terminem e coleta os resultados
    results = await asyncio.gather(*tasks)
    
    end_time = time.perf_counter()
    
    total_requests = sum(results)
    total_duration = end_time - start_time
    requests_per_second = total_requests / total_duration

    print("\n--- Resultados ---")
    print(f"Tempo total: {total_duration:.2f} segundos")
    print(f"Total de requisições bem-sucedidas: {total_requests}")
    print(f"Requisições por segundo (RPS): {requests_per_second:.2f}")

if __name__ == "__main__":
    asyncio.run(main())