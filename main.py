from socket import *
from threading import Thread

class Switch:
    def __init__(self, IP, plane_port, ground_port, data_max_recv, cmd_max_recv) -> None:
        self.plane_sock = socket(AF_INET, SOCK_DGRAM)
        self.ground_sock = socket(AF_INET, SOCK_DGRAM)
        self.plane_sock.bind((IP, plane_port))
        self.ground_sock.bind((IP, ground_port))

        self.data_max_recv = data_max_recv
        self.cmd_max_recv = cmd_max_recv

        self.plane_addr = None
        self.ground_addr = None


    def start(self):
        self.t_data = Thread(target=self._data_task)
        self.t_cmd = Thread(target=self._cmd_task)
        self.serve = True
        self.t_data.start()
        self.t_cmd.start()

    def stop(self):
        self.serve = False
        self.t_data.join()
        self.t_cmd.join()

    def _data_task(self):
        while self.serve:
            print("waiting data")
            data, self.plane_addr = self.plane_sock.recvfrom(self.data_max_recv)
            print("data", data)
            if self.ground_addr:
                self.ground_sock.sento(data, self.ground_addr)

    def _cmd_task(self):
        while self.serve:
            print("waiting cmd")
            cmd, self.ground_addr = self.ground_sock.recvfrom(self.cmd_max_recv)
            print("cmd", cmd)
            if self.plane_addr:
                self.plane_sock.sento(cmd, self.plane_addr)

if __name__ == "__main__":
    sw = Switch("192.168.219.105", 1234, 1235, 1024, 1024)
    sw.start()