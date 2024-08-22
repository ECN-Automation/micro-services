from granulometry import GranulometryService

if __name__ == "__main__":
    granulometry_service = GranulometryService(host="localhost", port=8083)
    granulometry_service.start()