import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' #hide pygame support prompt
import pygame
import files
from ctypes import windll, wintypes
import win32api
import win32con
import win32gui
import ctypes
from ctypes import wintypes


def getMouse():
    pt = wintypes.POINT()
    GetCursorPos(pt)
    return pt.x, pt.y

def moveWindow(new_x, new_y):
    w, h = pygame.display.get_surface().get_size()
    windll.user32.MoveWindow(hwnd, int(new_x), int(new_y), w, h, False)



class RECT(ctypes.Structure):
    _fields_ = [('left', wintypes.LONG),
                ('top', wintypes.LONG),
                ('right', wintypes.LONG),
                ('bottom', wintypes.LONG)]

class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('rcMonitor', RECT),
        ('rcWork', RECT),
        ('dwFlags', wintypes.DWORD)
    ]

def getTaskbarHeight():
    monitor = windll.user32.MonitorFromWindow(hwnd, 0x1)  
    
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    
    windll.user32.GetMonitorInfoW(monitor, ctypes.byref(mi))
    
    # Full monitor height vs work area height
    full_height = mi.rcMonitor.bottom - mi.rcMonitor.top
    work_height = mi.rcWork.bottom - mi.rcWork.top
    
    return full_height - work_height
    
def getScreenHeight():
    monitor = windll.user32.MonitorFromWindow(hwnd, 0x1)  
    
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    
    windll.user32.GetMonitorInfoW(monitor, ctypes.byref(mi))
    
    full_height = mi.rcMonitor.bottom - mi.rcMonitor.top
   
    return full_height 


def draw(character):
    SCREEN.blit(character, (0, 0))


def main(character_path):

    taskbar_height = getTaskbarHeight()
    screen_height = getScreenHeight()

    fuchsia = (255, 0, 128)  # Transparency color
    
    # Set window transparency color
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

    window_pos = [100, 100]
    moveWindow(*window_pos)

    dragging = False
    drag_offset = (0, 0)

    standby = "standby_mode"
    standby_path = os.path.join(character_path, standby)
    standby_index = files.countFiles(standby_path)
    standby_count = 0

    drift = "drift_mode"
    drift_path = os.path.join(character_path, drift)
    drift_index = files.countFiles(drift_path)
    drift_count = 0

    # Make window background transparent
    SCREEN.fill((fuchsia))

    while True:

        is_dragging = False

        for event in pygame.event.get():

            #check status of the window
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            #check for window movement
            if event.type == pygame.VIDEORESIZE:
                if not is_dragging:
                    is_dragging = True
                              
            #START drag on left button down 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gx, gy = getMouse()
                wx, wy = window_pos
                drag_offset = (gx - wx, gy - wy)
                dragging = True

            #STOP drag when button released
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False

        if dragging:
            #move window
            gx, gy = getMouse()
            window_pos[0] = gx - drag_offset[0]
            window_pos[1] = gy - drag_offset[1]
            moveWindow(*window_pos)

            #clear screen
            SCREEN.fill((fuchsia)) 

            #change character frame
            drift_file_path = os.path.join(drift_path, f"{drift_count}.png")
            character = pygame.image.load(drift_file_path ).convert_alpha()
            character = pygame.transform.scale(character, (screen_x, screen_y))
            draw(character)
            drift_count += 1
            if drift_count >= drift_index:
                drift_count = 0
        
        elif not dragging:
            #clear screen
            SCREEN.fill((fuchsia)) 

            #change character frame
            standby_file_path = os.path.join(standby_path, f"{standby_count}.png")
            character = pygame.image.load(standby_file_path ).convert_alpha()
            character = pygame.transform.scale(character, (screen_x, screen_y))
            draw(character)
            standby_count += 1
            if standby_count >= standby_index:
                standby_count = 0

        on_ground = True
        

        if window_pos[1] + screen_y < screen_height - taskbar_height:
            window_pos[1] += 1
            on_ground = False
        
        if not on_ground and not is_dragging:
            moveWindow(*window_pos)


        # Update display
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":

    current_dir = os.getcwd()
    if "OneDrive" in current_dir:
        # Change to C: drive
        new_dir = "C:\\desktop_pet"
        os.makedirs(new_dir, exist_ok=True)
        os.chdir(new_dir)
        print(f"Moved from OneDrive to: {new_dir}")


    pygame.init()
    clock = pygame.time.Clock()
    
    character_path = files.findCharacter()

    screen_x = 150
    screen_y = 150

    screen_x = int(input("How big would you want your pet be horizontially? (default 150) \nPlease enter a number greater than 0: "))
    if screen_x <= 0:
        screen_x = 150
    screen_y = int(input("How big would you want your pet be vertically? (default 150) \nPlease enter a number greater than 0: "))
    if screen_y <= 0:
        screen_y = 150

    fuchsia = (255, 0, 128)  # Transparency color

    SCREEN = pygame.display.set_mode((screen_x, screen_y), pygame.NOFRAME)
    SCREEN.set_alpha(None)  # Enable alpha
    # Create layered window
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

    # WinAPI: get global mouse position
    GetCursorPos = windll.user32.GetCursorPos
    GetCursorPos.argtypes = [wintypes.LPPOINT]


    # Set the window to stay on top
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)


    main(character_path)
    
