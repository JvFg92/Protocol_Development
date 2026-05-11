import socket
import struct

def empacotar_mensagem(msg_type, payload):
    payload_bytes = payload.encode('utf-8')
    length = len(payload_bytes)
    header = struct.pack('!BBH', 1, msg_type, length)
    return header + payload_bytes

def perguntar(pergunta, host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Envia a pergunta
        pacote = empacotar_mensagem(1, pergunta)
        s.sendall(pacote)
        
        # Recebe o cabeçalho da resposta
        header = s.recv(4)
        if not header:
            return "Erro na conexão"
            
        version, msg_type, length = struct.unpack('!BBH', header)
        
        # Recebe o payload (a resposta)
        resposta = s.recv(length).decode('utf-8')
        return resposta

if __name__ == "__main__":
    q = "Qual é a capital do Brasil?"
    print(f"Enviando: {q}")
    resp = perguntar(q)
    print(f"Servidor respondeu: {resp}")