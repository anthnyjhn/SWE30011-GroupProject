import serial
import time
import paho.mqtt.client as mqtt
import json

#
THINGSBOARD_SERVER = 'thingsboard.cloud'
ACCESS_TOKEN = 'opfrww192q88qvnmejgz' # DO NOT CHANGE THIS
SERIAL_PORT = '/dev/ttyS0' # change this as well
BAUD_RATE = 9600

# handles the commands coming from the dashboard
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    method = payload.get("method")
    print(f"Command received: {method}")
    
    if method == "setFan":
        if payload.get("params") is True:
            ser.write(b'4')
        else:
            ser.write(b'3')

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
    print(f"Could not connect to the cloud: {e}")
    exit()

# connect to arduino
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    print(f"Serial connection failed: {e}")
    print("Check if your Arduino is on /dev/ttyACM0 or /dev/ttyUSB0")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if "," in line:
                parts = line.split(',')
                if len(parts) == 3:
                    telemetry = {
                        "humidity": float(parts[0]),
                        "temperature": float(parts[1])
                    }
                    client.publish("v1/devices/me/telemetry", json.dumps(telemetry))
                    print(f"Sent to cloud: {telemetry}")
        time.sleep(0.1)
except KeyboardInterrupt:
    ser.close()
    client.disconnect()