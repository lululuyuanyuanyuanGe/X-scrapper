import subprocess
import time
from wxauto import WeChat
import pyautogui
import threading



wx = WeChat()
listen_list = ['Luyuan','高原']
process_map = {}

def listen_to_stdout(friend, process):
    """
    Listen to the subprocess's stdout and send each line to the friend.
    """
    while True:
        if process.poll() is not None:  # Check if the subprocess has terminated
            print(f"Subprocess for {friend} has terminated")
            break

        try:
            # Read one line from stdout
            data = process.stdout.readline().strip()  # Strip removes trailing newlines
            if data:
                print(f"Received from subprocess for {friend}: {data}")
                wx.SendMsg(data, friend)  # Send the line to the friend
                pyautogui.click(600, 300)
        except Exception as e:
            print(f"Error reading stdout for {friend}: {e}")
            break


def handle_incoming_message(friend, message):
    global process_map

    # Start a new subprocess for the friend if not already in process_map
    if friend not in process_map or process_map[friend].poll() is not None:
        process = subprocess.Popen(
            ["X:\\ANACONDA\\Environments\\X-scrapper\\python.exe", "X:\\CSProjects\\Python\\X-scrapper\\main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize = 0,
            encoding='utf-8'
        )

        process_map[friend] = process
        print(f"Started subprocess for {friend}")

        thread = threading.Thread(target=listen_to_stdout, args=(friend, process), daemon=True)
        thread.start()
    else:
        # Send the friend's message to the subprocess
        process = process_map[friend]
        process.stdin.write(f"{message}\n")
        process.stdin.flush()
        print(f"Sending message to subprocess for {friend}: {message}")

# Function to listen for new messages in WeChat
def listen_wechat():
    while True:
        msgs = wx.GetAllNewMessage()
        if msgs:
            for friend in listen_list:
                if friend in msgs:
                    for msg in msgs[friend]:
                        print(f"Received message from {friend}: {msg.content}")
                        handle_incoming_message(friend, msg.content)
                        pyautogui.click(600, 300)
        time.sleep(0.1)

# Start listening for WeChat messages
print("WeChat bot is running...")
listen_wechat()
