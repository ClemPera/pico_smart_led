class LEDs:
    def __init__(self, brightness = 10,rgb = (255,255,255),status = "OFF"):
        self.brightness = brightness
        self.rgb = rgb
        self.status = status
        
import time
import neopixel
from machine import Pin, WDT
import rp2
import network
from umqttsimple import MQTTClient
led_count = 150 # number of LEDs in ring light
PIN_NUM = 0 # pin connected to ring light

neo = neopixel.NeoPixel(Pin(0), 150)

leds = LEDs()

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user="", password="", keepalive=keep_alive)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    wdt.feed()
    
    client.disconnect()
    client_setup()

def client_setup():
    try:
        global client
        print("connecting and subscribing to mqtt")
        client = mqtt_connect()
        client.set_callback(new_message_callback)
        client.subscribe("brightness/set".encode('utf-8'))
        client.subscribe("rgb/set".encode('utf-8'))
        client.subscribe("light/switch".encode('utf-8'))
    except OSError as e:
        print("error connecting/subscribing to mqtt")
        reconnect()

# This code is executed once a new message is published
def new_message_callback(topic, msg):
    topic = topic.decode('utf-8')
    msg = msg.decode('utf-8')

    print("Topic: " + topic + " | Message: " + msg)
    
    if topic == "light/switch":
        light = msg
        checkStatus(light)
        client.publish("light/status".encode('utf-8'), msg)
        print("changed status")
        
    if topic == "rgb/set":
        rgb = tuple(map(int, msg.split(',')))
        client.publish("rgb/status".encode('utf-8'), msg)
        changeColor(rgb)
        print("changed rgb")
        
    if topic == "brightness/set":
        brightness = int(msg)
        client.publish("brightness/status".encode('utf-8'), msg)
        changeBrightness(brightness)
        print("changed brightness")
    
def checkStatus(status):
    if status == "OFF":
        changeBrightness(0)
    if status == "ON" and leds.brightness == 0:
        changeBrightness(10)
        
def changeBrightness(brightness):
    leds.brightness = brightness
    color = set_brightness(leds.rgb, brightness)
    neo.fill(color)
    neo.write()
    
def changeColor(color):
    leds.rgb = color
    color = set_brightness(color, leds.brightness)
    neo.fill(color)
    neo.write()
    
def set_brightness(color, brightness):
    r, g, b = color
    r = int(r * brightness/255)
    g = int(g * brightness/255)
    b = int(b * brightness/255)
    return (r, g, b)

def wifi_connect():
    try:
        global wlan
        print("connecting to wifi...")
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.config(pm = 0xa11140) # prevent the wireless chip from activating power-saving mode when it is idle
        wlan.ifconfig(('192.168.0.99', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
        wlan.connect("F For WiFi", "Procreate1!Driving!Disliking!Moonbeam!Reconcile")

        while True:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            print('waiting for connection...')
            wdt.feed()
            time.sleep(1)

        if wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = wlan.ifconfig()
            print( 'ip = ' + status[0] )

    except:
        print("wlan error")

wlan = None
wifi_connect()

#mqtt config
mqtt_server = 'broker.mqtt.cool'
client_id = 'PicoW'

last_message = 0
message_interval = 5
counter = 0

#hardware watchdog if the program crash, it restart completly
wdt=WDT(timeout=8388)
wdt.feed()

keep_alive=60 #set the seconds between 2 keep alive messages
client = None
client_setup()


last_message=time.time()

# Main loop
while True:
    try:
        client.check_msg()
    except OSError as e:
        print("error client.check_msg() : ", e)
        reconnect()
        pass
    
    wdt.feed()
    
    if not wlan.isconnected():
        wifi_connect()
        client_setup()

client.disconnect() #Never reached because of the infinite loop
print("end of code")
