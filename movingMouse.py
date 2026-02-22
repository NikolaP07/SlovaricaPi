import pyautogui
import keyboard

while True:
    key=keyboard.read_key()
    print(key)
    if key == "p":
        break
    if key=="left":
      print("left")
      pyautogui.move(-50, 0)
    if key=="down":
      print("down")
      pyautogui.move(0, 50)
    if key=="right":
      print("right")
      pyautogui.move(50, 0)
    if key=="up":
      print("up")  
      pyautogui.move(0, -50)    
