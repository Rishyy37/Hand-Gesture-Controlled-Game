import subprocess
import multiprocessing
import time
import os

def run_server():
    print("Starting game server...")
    os.chdir("Platformer_1")  
    subprocess.run(["python", "platformer.py"])


def run_client():
    print("Starting hand control client...")
    subprocess.run(["python", "hand_control_client/hand_controller.py"])


if __name__ == "__main__":
    server_process = multiprocessing.Process(target=run_server)
    client_process = multiprocessing.Process(target=run_client)

    server_process.start()
    client_process.start()

    server_process.join()
    client_process.join()
