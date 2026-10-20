import cv2
import os
import numpy as np
import pydirectinput as pdi
import pyautogui
import keyboard
import time

isScriptEnabled = False
reference_images_folder = "./reference_images"
reference_images = []
for filename in os.listdir(reference_images_folder):
  if filename.endswith('.png') or filename.endswith('.jpg'):
    img_path = os.path.join(reference_images_folder, filename)
    reference_images.append(cv2.imread(img_path))

def toggle_script():
  global isScriptEnabled
  isScriptEnabled = not isScriptEnabled
  print("Script is now ", "enabled" if isScriptEnabled else "disabled")
  
keyboard.add_hotkey('ctrl+shift+f', toggle_script)

while True:
  if isScriptEnabled:
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    
    for idx, ref_img in enumerate(reference_images):
      result = cv2.matchTemplate(screenshot_cv, ref_img, cv2.TM_CCOEFF_NORMED)
      min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
      threshold = 0.6
          
      if max_val > threshold:
        ref_h, ref_w, _ = ref_img.shape
        
        center_x = max_loc[0] + ref_w // 2
        center_y = max_loc[1] + ref_h // 2
        
        pdi.moveTo(center_x, center_y)
        pdi.moveRel(1)
        print(f"Deep pool found at coords x:{center_x} y: {center_y}")
        time.sleep(1)
      else:
        print(f"Scanning...")
  else:
    print("""
          Press CTRL + SHIFT + F to enable the script
          """) 
    keyboard.wait('ctrl+shift+f')
    
    
    
