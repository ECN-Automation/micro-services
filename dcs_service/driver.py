from communication import CommunicationService

if __name__ == "__main__":
    communication_service = CommunicationService(host="localhost", port=8084)
    communication_service.start()