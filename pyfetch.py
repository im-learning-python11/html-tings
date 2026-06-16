import psutil
import platform
import shutil
import socket
import datetime
import os
import getpass


class SystemInfo:
    def __init__(self):
        self.data = {}

    def collect(self):
        self.add_os_info()
        self.add_hardware_info()
        self.add_network_info()
        self.add_user_info()
        return self.data

    def add_os_info(self):
        self.data["OS"] = f"{platform.system()} {platform.release()}"
        self.data["Kernel"] = platform.version()
        self.data["Python"] = platform.python_version()

    def add_user_info(self):
        self.data["User"] = getpass.getuser()
        self.data["Hostname"] = socket.gethostname()

    def add_hardware_info(self):
        # CPU
        self.data["CPU"] = f"{platform.processor()} ({psutil.cpu_count()} cores)"
        self.data["CPU Load"] = f"{psutil.cpu_percent(interval=0.1)}%"

        # Memory
        mem = psutil.virtual_memory()
        self.data["RAM"] = f"{mem.used // 1024 ** 2}MB / {mem.total // 1024 ** 2}MB"

        # Disk
        disk = shutil.disk_usage("/")
        self.data["Disk"] = f"{disk.used // 1024 ** 3}GB / {disk.total // 1024 ** 3}GB"

        # Uptime
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        self.data["Uptime"] = str(uptime).split('.')[0]

    def add_network_info(self):
        # Get primary IPv4
        try:
            interfaces = psutil.net_if_addrs()
            for name, addrs in interfaces.items():
                for addr in addrs:
                    if addr.family == socket.AF_INET and addr.address != '127.0.0.1':
                        self.data["IP Address"] = addr.address
                        return
        except:
            self.data["IP Address"] = "N/A"


def run_fetch():
    fetcher = SystemInfo()
    info = fetcher.collect()

    print("\033[1;35m" + "=== [ ADVANCED SYSTEM REPORT ] ===" + "\033[0m")
    for key, value in info.items():
        print(f"\033[1;36m{key:<12}\033[0m: {value}")


if __name__ == "__main__":
    run_fetch()