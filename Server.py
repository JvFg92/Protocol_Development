import socket
import struct

# Dicionário simples de perguntas e respostas
BASE_DADOS = {
    "Qual é a capital do Brasil?": "Brasília",
    "Quanto é 2+2?": "4",
    "O que é HTTP?": "Hypertext Transfer Protocol"
}

def empacotar_mensagem(msg_type, payload):
    # ! = Network Byte Order (Big Endian), B = unsigned char (1 byte), H = unsigned short (2 bytes)
    payload_bytes = payload.encode('utf-8')
    length = len(payload_bytes)
    header = struct.pack('!BBH', 1, msg_type, length)
    return header + payload_bytes

def iniciar_servidor(host='0.0.0.0', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor SQAP ouvindo em {host}:{port}...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conectado a {addr}")
                # 1. Lê o cabeçalho (4 bytes)
                header = conn.recv(4)
                if not header:
                    continue
                
                version, msg_type, length = struct.unpack('!BBH', header)
                
                if msg_type == 1: # Se for uma requisição
                    # 2. Lê o payload baseado no tamanho do cabeçalho
                    payload = conn.recv(length).decode('utf-8')
                    print(f"Pergunta recebida: {payload}")
                    
                    # 3. Formula a resposta
                    resposta = BASE_DADOS.get(payload, "Desculpe, não sei a resposta.")
                    pacote_resposta = empacotar_mensagem(2, resposta)
                    
                    # 4. Envia de volta
                    conn.sendall(pacote_resposta)

if __name__ == "__main__":
    iniciar_servidor()