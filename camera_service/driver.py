from camera import CameraService

if __name__ == "__main__":
    camera_service = CameraService(host="localhost", port=8081)
    camera_service.start()