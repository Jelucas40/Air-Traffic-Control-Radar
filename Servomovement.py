from gpiozero import Servo
from time import sleep

# Initialize Servo on GPIO 14
servo = Servo(14)

# Servo Positions (Adjust these if needed for fine-tuning)
CENTER = 0        # Neutral (center) position
RIGHT_90 = 0.5    # Approximate 90° Right
LEFT_180 = -1     # Approximate 180° Left
RIGHT_180 = 1     # Approximate 180° Right

try:
    # Initial 90° Right Movement
    print("Moving servo 90° Right")
    servo.value = RIGHT_90
    sleep(1)
    
    while True:
        print("Moving servo 180° Left")
        servo.value = LEFT_180
        sleep(1)
        
        print("Moving servo 180° Right")
        servo.value = RIGHT_180
        sleep(1)
        
except KeyboardInterrupt:
    print("Program stopped by user")

