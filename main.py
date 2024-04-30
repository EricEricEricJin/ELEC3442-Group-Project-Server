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
            # print("wait...")
            try:
                data, self.plane_addr = self.plane_sock.recvfrom(self.data_max_recv)
                if self.ground_addr:
                    self.ground_sock.sendto(data, self.ground_addr)
                # print(len(data))
            except Exception as e:
                print("data err", e)

    def _cmd_task(self):
        while self.serve:
            try:
                cmd, self.ground_addr = self.ground_sock.recvfrom(self.cmd_max_recv)
                if self.plane_addr:
                    self.plane_sock.sendto(cmd, self.plane_addr)
            except Exception as e:
                print("cmd err", e)

IP = "154.221.20.43"
plane_port = 1234
ground_port = 1235

video_plane_port = 1236
video_ground_port = 1237

if __name__ == "__main__":
    import time 
    sw = Switch(IP, plane_port, ground_port, 1024, 1024)
    sw_video = Switch(IP, video_plane_port, video_ground_port, 1024*1024, 1024)
    sw.start()
    sw_video.start()

    # while True:
    #     print("plane", sw_video.plane_addr, "gnd", sw_video.ground_addr)
    #     time.sleep(1)
