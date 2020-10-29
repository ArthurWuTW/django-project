import os
import json

secuere_data_path = os.path.dirname(os.path.abspath(__file__))+"/secure_data.json"

print(secuere_data_path)

class SecureDataLoader():
    def __init__(self):
        with open(secuere_data_path, "r") as file:
            self.secure_data = json.load(file)
        print(self.secure_data)


if __name__ == '__main__':
    scdLoader = SecureDataLoader()
