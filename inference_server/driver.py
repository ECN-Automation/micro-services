from inference import InferenceService

if __name__ == "__main__":
    inference_service = InferenceService(host="localhost", port=8082)
    inference_service.start()