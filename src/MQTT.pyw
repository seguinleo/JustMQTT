import tkinter as tk
import paho.mqtt.client as mqtt

def on_subscribe(client, userdata, mid, granted_qos):
    nomTopic = zoneTopic.get()
    labelAbonnement.config(text = "" + nomTopic, fg = "blue")
    boutonMessage.config(state = "active")

def on_message(client, userdata, message):
    labelMessageRecu.config(text = "" + str(message.payload.decode("utf-8")), fg = "blue")

def fonctionIp():
    ip = zoneIP.get()
    client = mqtt.Client("PouletEnSlip")
    client.connect(ip)
    zoneIP.config(state = "disable")
    boutonIP.config(state = "disable")
    zoneTopic.config(state = "normal")
    boutonTopic.config(state = "active")

def souscrire():
    ip = zoneIP.get()
    client = mqtt.Client("PouletEnSlip")
    client.connect(ip)
    nomTopic = zoneTopic.get()
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.loop_start()
    client.subscribe(nomTopic)
    zoneMessage.config(state = "normal")

def publier():
    ip = zoneIP.get()
    client = mqtt.Client("PouletEnSlip")
    client.connect(ip)
    nomTopic = zoneTopic.get()
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.loop_start()
    client.subscribe(nomTopic)
    client.publish(nomTopic, zoneMessage.get())

fen = tk.Tk()
fen.geometry("810x475")
fen.title("MQTT")
fen.iconbitmap('icon.ico')
fen.resizable(False, False)

label = tk.Label(fen, text = "MQTT communication application", font = "size 14 underline", fg = "red")
label.grid(column = 0, row = 0, columnspan = 3, pady = 15)

label = tk.Label(fen, text = "Broker IP:", font = "size 12", fg = "blue")
label.grid(column = 0, row = 1, sticky = 'w', padx = 5)

zoneIP = tk.Entry(fen, width = "15", font = "size 12")
zoneIP.insert(0, "192.168.1.1")
zoneIP.grid(column = 0, row = 2, sticky = 'w', padx = 5, pady = 5)

boutonIP = tk.Button(fen, text = "Validate IP", font = "size 12", command = fonctionIp)
boutonIP.grid(column = 2, row = 2, sticky = 'e', padx = 5, pady = 5)

label = tk.Label(fen, text = "Topic name:", font = "size 12", fg = "blue")
label.grid(column = 0, row = 3, sticky = 'w', padx = 5)

zoneTopic = tk.Entry(fen, width = "30", font = "size 12", state = "disable")
zoneTopic.grid(column = 0, row = 4, sticky = 'w', padx = 5, pady = 5)

boutonTopic = tk.Button(fen, text = "Subscribe to topic", font = "size 12", command = souscrire, state = "disable")
boutonTopic.grid(column = 2, row = 4, sticky = 'e', padx = 5, pady = 5)

label = tk.Label(fen, text = "")
label.grid(column = 0, row = 5)

label = tk.Label(fen, text = "Subscription to topic:", font = "size 10")
label.grid(column = 0, row = 6, sticky = 'e', pady = 5)

labelAbonnement = tk.Label(fen, text = "No topic...", font = "size 10", fg = "grey", width = "30")
labelAbonnement.grid(column = 1, row = 6)

label = tk.Label(fen, text = "Message(s) received:", font = "size 10")
label.grid(column = 0, row = 7, sticky = 'e', pady = 5)

labelMessageRecu = tk.Label(fen, text = "No message...", font = "size 10", fg = "grey", width = "30")
labelMessageRecu.grid(column = 1, row = 7)

label = tk.Label(fen, text = "")
label.grid(column = 0, row = 8)

label = tk.Label(fen, text = "Enter your message:", font = "size 12", fg = "blue")
label.grid(column = 0, row = 9, sticky = 'w', padx = 5)

zoneMessage = tk.Entry(fen, width = "30", font = "size 12", state = "disable")
zoneMessage.grid(column = 0, row = 10, sticky = 'w', padx = 5, pady = 5)

boutonMessage = tk.Button(fen, text = "Send message", font = "size 12", command = publier, state = "disable")
boutonMessage.grid(column = 2, row = 10, sticky = 'e', padx = 5, pady = 5)

boutonQuitter = tk.Button(text = "X", font = "size 12", bg = '#FF5020', width = 6, command = fen.destroy)
boutonQuitter.grid(column = 2, row = 11, sticky = 'e', padx = 5)

label = tk.Label(text = "PouletEnSlip © 2022", font = "size 8")
label.grid(column = 0, row = 11, sticky = 'w')

fen.mainloop()