import usb.core
import usb.util
import curses  # For capturing key presses on Linux
import time

# USB Vendor & Product ID (Update if necessary)
VENDOR_ID = 0x2123
PRODUCT_ID = 0x1010

# USB Commands for movement and firing
COMMANDS = {
    "up":    [0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "down":  [0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "left":  [0x02, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "right": [0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "stop":  [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    "fire":  [0x02, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
}

# Find the USB device
device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if device is None:
    raise ValueError("Missile launcher not found!")

# Detach kernel driver if necessary
if device.is_kernel_driver_active(0):
    device.detach_kernel_driver(0)

# Set device configuration
device.set_configuration()

# Function to send USB command
def send_command(command):
    """Sends a USB command to the missile launcher."""
    device.ctrl_transfer(0x21, 0x09, 0x0200, 0, command)

# Function to capture keyboard input using curses
def main(stdscr):
    stdscr.clear()
    stdscr.addstr("Use arrow keys to move, Enter to fire, 'q' to quit.\n")
    stdscr.refresh()
    
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)  # Non-blocking input

    try:
        while True:
            key = stdscr.getch()
            if key == curses.ERR:  # No key pressed
                continue
            
            if key == curses.KEY_UP:
                send_command(COMMANDS["up"])
            elif key == curses.KEY_DOWN:
                send_command(COMMANDS["down"])
            elif key == curses.KEY_LEFT:
                send_command(COMMANDS["left"])
            elif key == curses.KEY_RIGHT:
                send_command(COMMANDS["right"])
            elif key == 10:  # Enter key to fire
                send_command(COMMANDS["fire"])
                time.sleep(3)  # Keep firing signal for 3 seconds
                send_command(COMMANDS["stop"])
            elif key == ord('q'):  # Quit
                break

            send_command(COMMANDS["stop"])  # Stop movement after key release

    finally:
        stdscr.keypad(False)
        curses.nocbreak()
        stdscr.clear()
        stdscr.refresh()

# Run the program
curses.wrapper(main)
print("Exiting...")

