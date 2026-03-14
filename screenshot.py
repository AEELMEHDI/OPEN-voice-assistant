import pyautogui
import os
import time

# Choose your specific directory
save_dir = r"C:\Users\hp\Pictures\screenshots_python"# Update this path to your desired directory for saving screenshots   

# Make sure the folder exists
os.makedirs(save_dir, exist_ok=True)

# Take screenshot
def screenshot():
    a = time.strftime("%Y-%m-%d_%H-%M-%S")
    myscreenshot = pyautogui.screenshot()
    b= f"screenshot_{a}.png"

    # Save inside your chosen directory
    file_path = os.path.join(save_dir, b)
    myscreenshot.save(file_path)

    