import subprocess
import multiprocessing
import time

def run_server():
    print("Starting game server...")
    subprocess.run(["python", "Game/shoot.py"])

def run_client():
    print("Starting hand control client...")
    subprocess.run(["python", "hand_control_client/hand_udp.py"])

if __name__ == "__main__":
    server_process = multiprocessing.Process(target=run_server)
    client_process = multiprocessing.Process(target=run_client)

    server_process.start()
    client_process.start()

    server_process.join()
    client_process.join()
