from .Client import Client


class RuleEngine:
    client_map = {}

    @staticmethod
    def init(device_list):
        for d in device_list:
            RuleEngine.add_client(d)

    @staticmethod
    def add_client(device):
        client = Client(device)
        RuleEngine.client_map[device.id] = client
        client.start()

    @staticmethod
    def update_client(device_id):
        client = RuleEngine.client_map[int(device_id)]
        client.version += 1
