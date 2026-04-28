import RPi.GPIO as GPIO
import time
import math

# --- Configuration ---
LEFT_WING_PIN = 18
RIGHT_WING_PIN = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_WING_PIN, GPIO.OUT)
GPIO.setup(RIGHT_WING_PIN, GPIO.OUT)

# Initialize PWM at 50Hz (Standard for Servos)
left_pwm = GPIO.PWM(LEFT_WING_PIN, 50)
right_pwm = GPIO.PWM(RIGHT_WING_PIN, 50)
left_pwm.start(0)
right_pwm.start(0)

def set_angle(pwm, angle, invert=False):
    """Translates 0-180 degrees into duty cycle"""
    if invert:
        angle = 180 - angle
    duty = angle / 18 + 2
    pwm.ChangeDutyCycle(duty)

def butterfly_mimic(duration_sec, speed=1.0):
    """
    speed: higher is faster flapping
    """
    start_time = time.time()
    
    print("Butterfly robot active...")
    
    while time.time() - start_time < duration_sec:
        t = time.time() * speed
        
        # Use a Sine wave to create fluid motion
        # Butterflies have a 'clapping' motion: 0 to 90 degrees
        flap_angle = (math.sin(t * 5) + 1) * 45 
        
        # Add a slight 'shiver' or 'tremble' common in butterflies
        tremble = math.sin(t * 20) * 2
        
        # Sync wings
        set_angle(left_pwm, flap_angle + tremble)
        set_angle(right_pwm, flap_angle + tremble, invert=True)
        
        time.sleep(0.02) # High frequency updates for smoothness

try:
    # Mimic for 30 seconds at a natural pace
    butterfly_mimic(30, speed=1.5)

except KeyboardInterrupt:
    print("Butterfly resting.")

finally:
    left_pwm.stop()
    right_pwm.stop()
    GPIO.cleanup()