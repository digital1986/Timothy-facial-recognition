import RPi.GPIO as GPIO
import time
import Adafruit_DHT

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins for Ultrasonic Sensor
TRIG = 23
ECHO = 24

# Set up GPIO pin for Buzzer
BUZZER = 21


TRACKER_PIN = 2  # Assuming the tracker sensor OUT pin is connected to GPIO17

# Set up GPIO pin for DHT22 Sensor
DHT_PIN = 22  # DHT22 data pin connected to GPIO4 (adjust if necessary)

# Setup GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(TRACKER_PIN, GPIO.IN)  # Set the tracker sensor pin as input

# Function to measure distance
def measure_distance():
    # Send a pulse to trigger the ultrasonic sensor
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.2)  # 10 microsecond pulse
    GPIO.output(TRIG, GPIO.LOW)
    
    # Wait for the echo pin to go HIGH
    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()
    
    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()
    
    # Calculate the pulse length
    pulse_duration = pulse_end - pulse_start
    
    # Calculate distance (in cm)
    distance = pulse_duration * 17150  # Speed of sound is 34300 cm/s
    distance = round(distance, 4)  # Round to 2 decimal places
    
    return distance

# Function to detect object using the line tracker sensor
def detect_object_with_tracker():
    # Read the output of the tracker sensor (HIGH means object detected)
    if GPIO.input(TRACKER_PIN):
        print("Object detected by tracker sensor!")
        return True  # Object detected
    else:
        return False  # No object detected
        print("Object detected by tracker sensor!")
    

# Function to read temperature and humidity from DHT22
def read_dht22():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT_PIN)
    
    # Check if the reading was successful
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.1f}C, Humidity: {humidity:.1f}%")
        return temperature, humidity
    else:
        print("Failed to get reading from DHT22 sensor!")
        return None, None

# Main loop
try:
    while True:
        # Measure distance using the ultrasonic sensor
        distance = measure_distance()
        
        if distance is not None:
            print(f"Measured Distance: {distance} cm")
            
            # If distance is less than 10 cm, sound the buzzer
            if distance < 10:
                GPIO.output(BUZZER, GPIO.HIGH)  # Turn on buzzer
            else:
                GPIO.output(BUZZER, GPIO.LOW)  # Turn off buzzer

        # Detect if an object is detected by the tracker sensor
        if detect_object_with_tracker():
            GPIO.output(BUZZER, GPIO.HIGH)  # Turn on buzzer if an object is detected by tracker
        
        # Read temperature and humidity from DHT22
        temperature, humidity = read_dht22()
        
        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")

        # Wait before measuring again
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()  # Clean up GPIO settings
