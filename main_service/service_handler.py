import socket
import struct
import threading
import queue
import pickle
# PUERTOS
PORT_CAMERA = 8081 
PORT_INFERENCE = 8082
PORT_GRANULOMETRY = 8083
PORT_DCS = 8084
puertos = [PORT_CAMERA, PORT_INFERENCE, PORT_GRANULOMETRY, PORT_DCS]

# SERVICE IDs
SERVICE_CAMERA = 0x01
SERVICE_INFERENCE = 0x02
SERVICE_GRANULOMETRY = 0x03
SERVICE_DCS = 0x04

# TYPE IDS
PACKET_IMAGE = 0x01
PACKET_INFERENCE = 0x02
PACKET_NUMERIC = 0x03
PACKET_TEST = 0x04

class ServiceHandler:
    def __init__(self, host="localhost", port="8080"):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        print(f"Servicio principal iniciado, escuchando en {self.port}")
    
    def send_payload(self, client_socket, payload, serviceID, typeID):
        payload_length = len(payload)
        header = struct.pack('>BB I', serviceID, typeID, payload_length)
        client_socket.sendall(header)
        client_socket.sendall(payload)
    
    def test_connections(self):
        for puerto in puertos:
            try:
                print(f"Probando conexión con puerto {puerto}...")
                send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send_socket.connect(("localhost", puerto))
                payload=pickle.dumps(1)
                payload_length = len(payload)
                header = struct.pack('>BB I', 0x00, 0x04, payload_length)
                send_socket.sendall(header)
                conn, addr = self.server_socket.accept()
                header = conn.recv(6)         
                print(header)
                service_id, packet_type, payload_length = struct.unpack('>BB I', header)
                payload = b''
                while len(payload) < payload_length:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    payload += chunk
                print(f"Conexión funcionando correctamente.")
            except Exception as e:
                print(f"Error en conexión")
                print(e)
                return False
            finally:
                send_socket.close()
        return True

    def start(self):
        if self.test_connections():
            print("Comenzando proceso...")
            # Enviar señal de inicio al servicio de cámara
            print("Enviando señal de inicio al servicio de cámara")
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.connect(("localhost", PORT_CAMERA))
            payload="start"
            payload_length = len(payload)
            header = struct.pack('>BB I', 0x00, 0x00, payload_length)
            send_socket.sendall(header)
            send_socket.close()
            while True:
                # Recibimos información desde una conexión
                print("Esperando conexión...")
                conn, addr = self.server_socket.accept()
                header = conn.recv(6)         
                service_id, packet_type, payload_length = struct.unpack('>BB I', header)
                payload = b''
                while len(payload) < payload_length:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    payload += chunk
                
                if service_id == SERVICE_CAMERA:
                    print("Imagen recibida.")
                    print("Enviando imagen para inferencia")
                    try:
                        # Connect to the server
                        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        send_socket.connect(("localhost", PORT_INFERENCE))
                        
                        # Send the image
                        send_payload(send_socket, payload)

                        print("Imagen enviada para inferencia.")
                    finally:
                    # Close the socket
                        send_socket.close()
                
                if service_id == SERVICE_INFERENCE:
                    print("Inferencias recibidas")
                    print("Enviando inferencias para cálculo de granulometría")
                    try:
                        # Connect to the server
                        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        send_socket.connect(("localhost", PORT_GRANULOMETRY))
                        
                        # Send the image
                        send_payload(send_socket, payload)

                        print("Inferencias enviadas para calculo granulométrico.")
                    finally:
                    # Close the socket
                        send_socket.close()

                if service_id == SERVICE_DCS:
                    print("Información granulométrica recibida.")
                    print("Enviando información para comunicación DCS")
                    try:
                        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        send_socket.connect(("localhost", PORT_DCS))
                        send_payload(send_socket, payload)

                        print("Inferencias enviadas para calculo granulométrico.")
                    finally:
                    # Close the socket
                        send_socket.close()
                        print("Enviando señal de inicio al servicio de cámara")
                        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        send_socket.connect(("localhost", PORT_CAMERA))
                        payload="start"
                        payload_length = len(payload)
                        header = struct.pack('>BB I', 0x00, 0x00, payload_length)
                        send_socket.sendall(header)
                        send_socket.close()