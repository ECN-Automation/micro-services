from service_handler import ServiceHandler

if __name__ == "__main__":
    service_handler = ServiceHandler(host="localhost", port=8080)
    service_handler.start()