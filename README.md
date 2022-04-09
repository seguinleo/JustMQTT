# MQTT
MQTT Client HMI built in Python to communicate via a Broker

```python
import tkinter as tk
import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    labelMessageRecu.config(text="" + str(message.payload.decode("utf-8")), fg="blue")

def on_subscribe(client, userdata, mid, granted_qos):
    nomTopic=zoneTopic.get()
    labelAbonnement.config(text="" + nomTopic, fg="blue")
    boutonMessage.config(state="active")

def souscrire():
    nomTopic=zoneTopic.get()
    client.subscribe(nomTopic)

def publier():
    client.publish("pouletTopic",zoneMessage.get())

#Configuration
broker_address=""
client=mqtt.Client("")
client.connect(broker_address)
client.on_message=on_message
client.on_subscribe=on_subscribe
client.loop_start()

fen=tk.Tk()
fen.geometry("494x330")
fen.title("MQTT")

labelTitre=tk.Label(fen, text="MQTT communication application", font="size 14", fg="red")
labelTitre.grid(column=0, row=0, columnspan=3, pady=15)

label=tk.Label(fen, text="Topic name :", font="size 12", fg="blue")
label.grid(column=0, row=1, sticky='w', padx=5)

zoneTopic=tk.Entry(fen, width="20", font="size 12")
zoneTopic.grid(column=0, row=2, sticky='w', padx=5, pady=5)

boutonMessage=tk.Button(fen, text="Subscribe to the topic", font="size 12", command=souscrire)
boutonMessage.grid(column=2, row=2, sticky='e', padx=5, pady=5)

labelVide=tk.Label(fen, text="")
labelVide.grid(column=0, row=3)

labelSouscription=tk.Label(fen, text="Subscription to topic :", font="size 10")
labelSouscription.grid(column=0, row=4, sticky='e', pady=5)

labelAbonnement=tk.Label(fen, text="No topic...", font="size 10", fg="grey", width="15")
labelAbonnement.grid(column=1, row=4)

label=tk.Label(fen, text="Message(s) received :", font="size 10")
label.grid(column=0, row=5, sticky='e', pady=5)

labelMessageRecu=tk.Label(fen, text="No message...", font="size 10", fg="grey", width="15")
labelMessageRecu.grid(column=1, row=5)

labelVide=tk.Label(fen, text="")
labelVide.grid(column=0, row=6)

label=tk.Label(fen, text="Enter your message :", font="size 12", fg="blue")
label.grid(column=0, row=7, sticky='w', padx=5)

zoneMessage=tk.Entry(fen, width="20", font="size 12")
zoneMessage.grid(column=0, row=8, sticky='w', padx=5, pady=5)

boutonMessage=tk.Button(fen, text="Send message", font="size 12", command=publier, state="disable")
boutonMessage.grid(column=2, row=8, sticky='e', padx=5, pady=5)

boutonQuitter=tk.Button(text="X", font="size 12", bg='#FF5020', width=6, command=fen.destroy)
boutonQuitter.grid(column=2, row=9, sticky='e', padx=5)

labelSign=tk.Label(text="by PouletEnSlip © 2022", font="size 7")
labelSign.grid(column=0, row=9, sticky='w')

fen.mainloop()
```
![0](https://github.com/PouletEnSlip/MQTT/blob/main/mqtt.png)

Made by **PouletEnSlip** © 2022 - All Rights Reserved
