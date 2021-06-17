import win32api
import time
from threading import Timer
from pynput import keyboard
import threading

PAUSE_SET_POS_BACK = 0.1
CYCLE_DELAY = 3.0

isFutureClickActive = False
isClicerkProgramActive = False

ACTIVATION_TOGGLE_COMBINATION = {
  keyboard.Key.ctrl_l, 
  keyboard.Key.alt_l, 
  keyboard.Key.space
}

# The currently active modifiers
current = set()

savedpos = win32api.GetCursorPos()

def moveMouse():
  global isFutureClickActive, savedpos
  x, y = win32api.GetCursorPos()
  win32api.SetCursorPos((x + 1,y))
  time.sleep(PAUSE_SET_POS_BACK)
  win32api.SetCursorPos((x,y))
  isFutureClickActive = False
  savedpos = win32api.GetCursorPos()
  print("moved!")

async def main():
  global isFutureClickActive, savedpos
  while isClicerkProgramActive == True:
    curpos = win32api.GetCursorPos()
    if savedpos == curpos:
      if isFutureClickActive == False:
        t = Timer(CYCLE_DELAY, moveMouse)
        t.start()
        isFutureClickActive = True
    else:
      if isFutureClickActive == True:
        t.cancel()
        isFutureClickActive = False
      savedpos = win32api.GetCursorPos()
    time.sleep(CYCLE_DELAY)

def on_press(key):
  global isClicerkProgramActive
  # print(key)
  if key in ACTIVATION_TOGGLE_COMBINATION:
    current.add(key)
    print(current)
    if all(k in current for k in ACTIVATION_TOGGLE_COMBINATION):
      current.clear()
      print('All modifiers active!')
      isClicerkProgramActive = not isClicerkProgramActive
      x = threading.Thread(target=main())
      if isClicerkProgramActive:
        x.start() 
      else: 
        x.join()
      print('Clicker is', 'active' if isClicerkProgramActive else 'inactive')
  

print('Starting...')

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread

print('Waiting for activation...')

listener.join()  # remove if main thread is polling self.keys
