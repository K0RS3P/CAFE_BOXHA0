import json
import csv

class FileManager:
    @staticmethod
    def save_to_json(data, file_path):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_from_json(path):
        with open(path, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_to_csv(data, file_path):
        if isinstance(data, dict):
            data = [data]  
        
        if not data:
            return

        headers = data[0].keys()
        
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def load_from_csv(path):
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)
