import serial
import time
import paho.mqtt.client as mqtt
import json

# config
THINGSBOARD_SERVER = 'thingsboard.cloud'
ACCESS_TOKEN = "8iahwr7cej2nfykeebt5" # DO NOT CHANGE THIS
SERIAL_PORT = '/dev/ttyS0' # change this as well
BAUD_RATE = 9600

# handle rpc
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        method = payload.get("method")
        print(f"Command received: {method}")
        
        if method == "setPump":
            if payload.get("params") is True:
                print("Turning Pump ON")
                ser.write(b"PUMP_ON\n")
            else:
                print("Turning Pump OFF")
                ser.write(b"PUMP_OFF\n")
    except Exception as e:
        print(f"Error processing command: {e}")

# setup mqtt
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.on_message = on_message

# connect to thingsboard
try:
    client.connect(THINGSBOARD_SERVER, 1883, 60)
    client.subscribe("v1/devices/me/rpc/request/+")
    client.loop_start()
    print("Connected to Thingsboard successfully")
except Exception as e:
    print(f"Cloud connection failed: {e}")
    exit()

# Connect to Arduino
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    print(f"Serial connection failed: {e}")
    print("Check if your Arduino is connected and the port is correct.")

try:
    while True:
        if ser.in_waiting > 0:
            # Ben: arduino sends: "MOISTURE=50"
            line = ser.readline().decode('utf-8').strip()
            
            if "MOISTURE=" in line:
                try:
                    value = int(line.split('=')[1])
                    telemetry = {"moisture": value}
                    
                    client.publish("v1/devices/me/telemetry", json.dumps(telemetry))
                    print(f"Sent: {telemetry}")
                except:
                    pass
        time.sleep(0.1)

except KeyboardInterrupt:
    ser.close()
    client.disconnect()
    print("\nGateway stopped.")