import serial
import time
import paho.mqtt.client as mqtt
import json

# config
THINGSBOARD_SERVER = 'thingsboard.cloud'
ACCESS_TOKEN = '3hgwhna454mn53lzgjs9' # DO NOT CHANGE THIS
SERIAL_PORT = '/dev/ttyS0' # change this 
BAUD_RATE = 9600
IsActuatorOn = False

# handle rpc
def on_message(client, userdata, msg):
    global IsActuatorOn

    try:
        payload = json.loads(msg.payload.decode())
        method = payload.get("method")
        print(f"Command received: {method}")
        
        if method == "setLed":
            if payload.get("params") is True:
                print("Turning LED ON")
                ser.write(b"LED=ON\n")
                IsActuatorOn = True
            else:
                print("Turning LED OFF")
                ser.write(b"LED=OFF\n")
                IsActuatorOn = False
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

try:
    while True:
        if ser.in_waiting > 0:
            # Sam: Arduino sends: "NODE=sam,SENSOR=ldr,VALUE=123"
            line = ser.readline().decode('utf-8').strip()
            
            if "VALUE=" in line:
                try:
                    parts = line.split(',')
                    val = 0
                    for part in parts:
                        if "VALUE=" in part:
                            val = int(part.split('=')[1])
                    
                    telemetry = {"lightLevel": val, "isActuatorOn": IsActuatorOn}
                    
                    client.publish("v1/devices/me/telemetry", json.dumps(telemetry))
                    print(f"Sent: {telemetry}")
                except:
                    pass
        time.sleep(0.1)

except KeyboardInterrupt:
    ser.close()
    client.disconnect()
    print("\nGateway stopped.")