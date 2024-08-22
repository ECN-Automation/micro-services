import socket
import struct
import pickle
import time
import cv2

# Configuration
SERVER_ADDRESS = ('localhost', 8080)
# Testing
IMAGE_PATH = '../test.jpg'  # Path to the image file to be sent
IMAGE_SEND_INTERVAL = 1  # Interval in seconds between sending images
TESTING = True
class CameraService:
    def __init__(self, host = "localhost", port="8081"):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        print(f"Servicio de camara iniciado, escuchando en {self.port}")

    def send_image(self, client_socket, image):
        # Serializamos la imagen
        serialized_image = pickle.dumps(image)
        # Creamos el header
        service_id = 0x01  # ID del servicio de camara
        packet_type = 0x01  # Tipo imagen
        payload_length = len(serialized_image)
        header = struct.pack('>BB I', service_id, packet_type, payload_length)
        client_socket.sendall(header)
        client_socket.sendall(serialized_image)

    def start(self):
        print("Esperando la prueba...")
        conn, addr = self.server_socket.accept()
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
            try:
                if TESTING:
                    image = cv2.imread(IMAGE_PATH)
                    client_socket.connect(SERVER_ADDRESS)
                    send_image(client_socket,image)
            except Exception as e:
                print(f"Error en conexión: {e}")
            finally:
                client_socket.close()

