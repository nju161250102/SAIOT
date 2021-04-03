from Client import Client


class RuleEngine:

    def __init__(self, device_list):
        self.client_map = {}
        for d in device_list:
            self.add_client(d)

    def add_client(self, device):
        client = Client(device.name)
        self.client_map[device.id] = client
        client.start()

    def update_client(self, device_id):
        client = self.client_map[device_id]
        client.version += 1