import pygame
import math
import random
from time import sleep
from gpiozero import DistanceSensor, Servo
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# GPIO Setup for the sonar
sensor = DistanceSensor(echo=24, trigger=23)  # HC-SR04 Sensor
servo = Servo(14)  # Servo on GPIO pin 14

# I2C Setup for the Pan-Tilt HAT
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Set frequency to 50 Hz for servos

# Function to set servo angle on Pan-Tilt HAT
def set_servo_angle(channel, pulse_us):
    """Set the servo pulse width in microseconds."""
    pulse_length = (pulse_us * 65535) // 20000  # Conversion to duty cycle
    pca.channels[channel].duty_cycle = int(pulse_length)

# Pygame Setup
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shader-Style Radar Display')
font = pygame.font.SysFont('Arial', 20)
small_font = pygame.font.SysFont('Arial', 16)

# Colors
BLACK = (0, 0, 0)
DARK_GREEN = (0, 50, 0)
GRID_GREEN = (0, 100, 0)
SWEEP_GREEN = (0, 255, 0, 200)  # Slightly transparent sweep
SWEEP_RED = (255, 0, 0, 200)    # Red sweep for detection
RED = (255, 0, 0)
WHITE = (255, 255, 255)
LIGHT_RED = (255, 22, 22)  # Light red for detection background

# Radar Configuration
RADIUS = 250
CENTER_X, CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50

# Detection Threshold
DETECTION_DISTANCE = 27.56  # inches (converted from 70 cm)

# Initialize radar history surface for fading trails
history_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
history_surface.fill((0, 0, 0, 0))

# Measure Distance Function
def measure_distance():
    """Measure distance from the ultrasonic sensor and return in inches."""
    return round(sensor.distance * 39.37, 2)  # Convert to inches

# Radar Grid with Radius Labels
def draw_radar_grid():
    """Draw the static shader-style radar grid with radius labels."""
    for i in range(1, 5):
        radius = 25 * i  # Start at 25 inches and increment by 25 inches
        adjusted_radius = int((radius / 100) * RADIUS)  # Scale radius properly
        pygame.draw.circle(screen, GRID_GREEN, (CENTER_X, CENTER_Y), adjusted_radius, 1)
        
        # Place radius label at the top center of each circle
        label = small_font.render(f'{radius} in', True, WHITE)
        label_x = CENTER_X - (label.get_width() // 2)
        label_y = CENTER_Y - adjusted_radius - 10  # Slight offset above the circle
        screen.blit(label, (label_x, label_y))

    # Radial lines
    for angle in range(0, 360, 30):
        angle_rad = math.radians(angle)
        end_x = CENTER_X + int(RADIUS * math.cos(angle_rad))
        end_y = CENTER_Y - int(RADIUS * math.sin(angle_rad))
        pygame.draw.line(screen, GRID_GREEN, (CENTER_X, CENTER_Y), (end_x, end_y), 1)

# Radar Sweep
def draw_radar_sweep(angle, distance):
    """Draw the dynamic shader-style radar sweep."""
    global history_surface

    angle_rad = math.radians(angle)
    end_x = CENTER_X + int(RADIUS * math.cos(angle_rad))
    end_y = CENTER_Y - int(RADIUS * math.sin(angle_rad))

    sweep_color = SWEEP_GREEN  # Default sweep color is GREEN

    # Check for object detection within threshold
    if distance <= DETECTION_DISTANCE:
        sweep_color = SWEEP_RED  # Change sweep color to red on detection

        # Plot detected object
        obj_x = CENTER_X + int((distance / 100) * RADIUS * math.cos(angle_rad))
        obj_y = CENTER_Y - int((distance / 100) * RADIUS * math.sin(angle_rad))
        pygame.draw.circle(screen, RED, (obj_x, obj_y), 5)

        # Persist object in the history surface
        pygame.draw.circle(history_surface, (255, 0, 0, 50), (obj_x, obj_y), 5)

    # Draw the sweep line
    pygame.draw.line(screen, sweep_color, (CENTER_X, CENTER_Y), (end_x, end_y), 2)

    # Fade the trail for a smoother effect
    history_surface.fill((0, 0, 0, 10), special_flags=pygame.BLEND_RGBA_MULT)

    # Blend history surface onto the main screen
    screen.blit(history_surface, (0, 0))

# Main Radar Loop
def radar_scan():
    try:
        angle = 0
        direction = 1  # 1 for increasing angle, -1 for decreasing

        while True:
            # Move servo for distance sensor
            target_value = (angle - 90) / 90  # Map angle to servo range (-1 to 1)
            servo.value = target_value

            # Move the pan-tilt HAT at the same pace as the servo
            tilt_angle = 1500 + int(target_value * 500)  # Adjust tilt for smooth movement
            pan_angle = 1500  # Keep pan centered

            # Set the Pan-Tilt HAT pan and tilt servos
            set_servo_angle(1, tilt_angle)  # Tilt (up/down)
            set_servo_angle(0, pan_angle)   # Pan (left/right)

            # Measure Distance
            distance = measure_distance()
            screen.fill(BLACK)  # Always keep background black

            # Draw Radar Elements
            draw_radar_grid()
            draw_radar_sweep(angle, distance)

            # Display Text Info
            text = font.render(f'Angle: {angle}° Distance: {distance} in', True, WHITE)
            screen.blit(text, (10, 10))

            # Refresh Display
            pygame.display.flip()

            # Update angle continuously
            angle += direction
            if angle >= 180 or angle <= 0:
                direction *= -1

            sleep(0.01)  # Smooth movement

    except KeyboardInterrupt:
        print("Radar stopped by user")
    finally:
        pygame.quit()

# Run the Radar
if __name__ == '__main__':
    radar_scan()
