import csv
import requests
import time
import threading

config_file = "balancer.csv"


class Server:
    def __init__(self, url):
        self.url = url
        self.alert = False
        self.status = True
        # creating a lock
        self.lock = threading.Lock()

    def __str__(self):
        return self.url

    def ping(self):
        try:
            payload = ""
            headers = {}

            response = requests.request("GET", self.url, headers=headers, data=payload)
            self.lock.acquire()
            self.status = response.status_code
            self.alert = False
            self.lock.release()
            return True
        except Exception as e:
            self.lock.acquire()
            self.status = str(e)
            self.alert = True
            self.lock.release()
            return False

    def is_server_up(self):
        self.lock.acquire()
        return not self.alert
        self.lock.release()


class Balancer:
    def __init__(self):
        self.servers = self.read_config()


    def read_config(self):
        csvFile = []
        # opening the CSV file
        D = {}

        with open(config_file, mode='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)

            # displaying the contents of the CSV file
            for lines in csvFile:
                print(lines)
                D[lines[0].lower().strip()] = Server(lines[1])

        return D

    def get_server(self, data):
        temp_data = data.lower().strip()
        if temp_data:
            print(f"Server for {data} -> {str(self.servers.get(temp_data))}")
            return self.servers.get(temp_data)
        return None

    def get_list_of_servers(self):
        print("List of servers are as follows")
        for v in self.servers.values():
            print(v)

    def health_check(self):
        while True:

            for k, v in self.servers.items():
                status = v.ping()
                print(f"{k} - connection status {status}")

            time.sleep(5)


balancer = Balancer()
t1 = threading.Thread(target=balancer.health_check())
t1.start()

if __name__ == "__main__":

    print("hi!")

