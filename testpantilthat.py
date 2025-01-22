from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from time import sleep

# Initialize the I2C bus and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Set frequency to 50 Hz for servos

# Function to convert microseconds to PWM duty cycle
def set_servo_angle(channel, pulse_us):
    """
    Set the servo pulse width in microseconds.
    :param channel: PCA9685 channel (0-15)
    :param pulse_us: Pulse width in microseconds (1000 to 2500)
    """
    pulse_length = (pulse_us * 65535) // 20000  # Conversion to duty cycle
    pca.channels[channel].duty_cycle = int(pulse_length)

try:
    print("Start")

    # Infinite loop to keep the servo moving continuously
    while True:
        # Pan servo centered (no movement), tilt servo moves between extremes
        set_servo_angle(0, 1500)  # Pan centered
        set_servo_angle(1, 1000)  # Tilt left (1000 µs)
        sleep(0.05)  # Quick movement (50 ms delay)
        
        set_servo_angle(1, 2000)  # Tilt right (2000 µs)
        sleep(0.05)  # Quick movement (50 ms delay)

        # Tilt servo continuously moving up and down between extremes
        set_servo_angle(0, 1000)  # Pan left (1000 µs)
        set_servo_angle(1, 1000)  # Tilt left (1000 µs)
        sleep(0.05)  # Quick movement (50 ms delay)
        
        set_servo_angle(0, 2000)  # Pan right (2000 µs)
        set_servo_angle(1, 2000)  # Tilt right (2000 µs)
        sleep(0.05)  # Quick movement (50 ms delay)

except KeyboardInterrupt:
    # Clean up and stop the servo movement when interrupted
    print("Stopping continuous movement")
    set_servo_angle(0, 1500)  # Reset pan servo to center
    set_servo_angle(1, 1500)  # Reset tilt servo to center
    pca.deinit()
    print("Finished")

