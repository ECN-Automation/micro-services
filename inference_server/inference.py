# yolo_service.py
import socket
import struct
import pickle
from ultralytics import YOLO

# Configuration
SERVER_ADDRESS = ('localhost', 8080)

SERVICE_ID = 0x02  # YOLO Service
PACKET_TYPE_IMAGE = 0x01
PACKET_TYPE_INFERENCE = 0x02

class InferenceService:
    def __init__(self, host = "localhost", port="8082"):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        print(f"Servicio de inferencia iniciado, escuchando en {self.port}")
    
    def send_payload(self, client_socket, payload):
        payload_length = len(payload)
        header = struct.pack('>BB I', SERVICE_ID, PACKET_TYPE_INFERENCE, payload_length)
        client_socket.sendall(header)
        client_socket.sendall(payload)
    
    def process_image(self, image):
        # Dummy YOLO processing (replace with actual YOLO code)
        return "YOLO inferences"

    def start(self):
        print("Esperando la prueba...")
        conn, addr = self.server_socket.accept()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(SERVER_ADDRESS)
        header = conn.recv(6)         
        service_id, packet_type, payload_length = struct.unpack('>BB I', header)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if packet_type==0x04:
            client_socket.connect(SERVER_ADDRESS)
            print("Paquete de prueba recibido")
            payload=pickle.dumps(1)
            payload_length = len(payload)
            header = struct.pack('>BB I', 0x00, 0x04, payload_length)
            client_socket.sendall(header)
            client_socket.close()
        while True:
            conn, addr = self.server_socket.accept()
            header = conn.recv(6)         
            service_id, packet_type, payload_length = struct.unpack('>BB I', header)
            
            payload = b''
            while len(payload) < payload_length:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                payload += chunk
            try:
                client_socket.connect(SERVER_ADDRESS)
                send_payload(client_socket,payload)
            except Exception as e:
                print(f"Error en conexión")
            finally:
                client_socket.close()
