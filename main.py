import paho.mqtt.client as mqtt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

# Define MQTT broker and topics
broker_address = "broker.emqx.io"  # Replace with your MQTT broker address
slot1_topic = "slot1"
slot2_topic = "slot2"
slot3_topic = "slot3"

# Create a dictionary to store slot statuses
slot_statuses = {
    slot1_topic: "Unknown",
    slot2_topic: "Unknown",
    slot3_topic: "Unknown"
}

# Create dictionaries to store slot labels and images
slot_labels = {}
slot_images = {}


# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed. Return code: " + str(rc))

    # Subscribe to parking slot topics
    client.subscribe(slot1_topic)
    client.subscribe(slot2_topic)
    client.subscribe(slot3_topic)


def on_message(client, userdata, msg):
    topic = msg.topic
    status = msg.payload.decode()
    slot_statuses[topic] = status
    update_gui()



# Create a function to update the GUI based on slot statuses
def update_gui():
    for slot, status in slot_statuses.items():
        label = slot_labels[slot]
        image = slot_images[slot]
        if status == "1":
            label.text = f"{slot} Parked"
            image.source = f"{slot}car_parked.png"
        elif status == "0":
            label.text = f"{slot} Free"
            image.source = f"{slot}car_free.png"
        else:
            label.text = f"{slot} Unknown"
            image.source = "unknown.jpg"


# Create an MQTT client
client = mqtt.Client()

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, 1883, 60)


# Create a Kivy app
class ParkingApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        for slot in slot_statuses:
            label = Label(text=f"{slot} Unknown", halign='center', valign='middle')
            image = Image(source="unknown.jpg")  # Default image for unknown state
            layout.add_widget(label)
            layout.add_widget(image)
            slot_labels[slot] = label
            slot_images[slot] = image
        return layout


if __name__ == '__main__':
    app = ParkingApp()
    app.run()
