# Instructions
**NOTE:** The python code is designed for the sketches you uploaded. so please dont change it without letting me know.

## Download Code
Get the python code located in /py folder. Dont run it yet.

## Local setup
Install these required python libraries:
- Serial for arduino
- MQTT to interact with Thingsboard

```bash
pip install pyserial tb-mqtt-client
```

## Thingsboard Setup
IMPORTANT: Copy your ACCESS CODE from your python code and replace the XXXXXX in the link below. Run the command in terminal

Windows, Linux or MacOS: 
```bash
curl -v -X POST http://thingsboard.cloud/api/v1/XXXXXXXXX/telemetry --header Content-Type:application/json --data "{temperature:25}"
```
In Linux, you might need to install curl
```bash
sudo apt-get install curl
```

**After running it please screenshot the result and notify me on Discord.**

## Run the python code:
```bash
python3 yourname_gateway.py
```

and you should see something like this:
```bash
admin@raspberry:~/Workspace/group_project/py $ python3 anthony_gateway.py
/home/admin/Workspace/group_project/py/anthony_gateway.py:25: DeprecationWarning: Callback API version 1 is deprecated, update to latest version
  client = mqtt.Client()
Connected to Thingsboard successfully
Connected to Arduino on /dev/ttyS0
Sent to cloud: {'humidity': 49.0, 'temperature': 23.8}
```









