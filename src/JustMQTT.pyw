import tkinter as tk
import paho.mqtt.client as mqtt
import os

def get_credentials():
    if os.path.isfile("settings.txt") == True:
        file = "settings.txt"
        with open(file, "r") as f:
            lines = f.readlines()
            username = lines[0].strip()
            ip = lines[1].strip()
            zoneUsername.insert(0, username)
            zoneIP.insert(0, ip)
    else:
        zoneUsername.insert(0, "user123")
        zoneIP.insert(0, "192.168.1.10")

def get_topic():
    if os.path.isfile("settings.txt") == True:
        with open("settings.txt", "r") as f:
            lines = f.readlines()
            if len(lines) > 2:
                topic = lines[2].strip()
                zoneTopic.insert(0, topic)
            else:
                zoneTopic.insert(0, "")
    else:
        zoneTopic.insert(0, "")

def send_info():
    user = zoneUsername.get().strip()
    ip = zoneIP.get().strip()
    if len(user) == 0:
        return
    if len(ip) == 0:
        return
    client = mqtt.Client(user)
    try:
        client.connect(ip)
        errorLabel.config(text="")
        zoneUsername.config(state="disable")
        zoneIP.config(state="disable")
        buttonIP.config(state="disable")
        zoneTopic.config(state="normal")
        buttonTopic.config(state="active")
        file = "settings.txt"
        if os.path.isfile("settings.txt") == True:
            with open(file, "r") as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    topic = lines[2].strip()
                    zoneTopic.insert(0, topic)
                else:
                    zoneTopic.insert(0, "")
            with open(file, "w") as f:
                f.write(user + "\n" + ip)
                f.close()
        else:
            with open(file, "w") as f:
                f.write(user.strip() + "\n" + ip.strip())
                f.close()
    except OSError as e:
        errorLabel.config(text=e)

def on_message(client, userdata, message):
    messageReceived=message.payload.decode("utf-8").strip()
    if len(messageReceived) == 0:
        return
    if len(messageReceived) > 1000:
        return
    getMessageLabel.config(state="normal")
    getMessageLabel.insert("end", messageReceived + "\n")
    getMessageLabel.config(state="disable")

def subscribe_topic():
    user=zoneUsername.get().strip()
    ip=zoneIP.get().strip()
    if len(user) == 0:
        return
    if len(ip) == 0:
        return
    client=mqtt.Client(user)
    try:
        client.connect(ip)
        topicName=zoneTopic.get().strip()
        if len(topicName) == 0:
            return
        client.loop_start()
        client.subscribe(topicName)
        client.on_message=on_message
        zoneMessage.config(state="normal")
        buttonSend.config(state="active")
        errorLabel.config(text="")
        file = "settings.txt"
        with open(file, "r") as f:
            lines = f.readlines()
            if len(lines) >= 3:
                lines[2] = topicName
                with open(file, "w") as f:
                    f.writelines(lines)
                    f.close()
            else:
                with open(file, "a") as f:
                    f.write("\n" + topicName)
                    f.close()
    except OSError as e:
        errorLabel.config(text=e)

def publish_message():
    user=zoneUsername.get().strip()
    ip=zoneIP.get().strip()
    client=mqtt.Client(user)
    if len(user) == 0:
        return
    if len(ip) == 0:
        return
    try:
        client.connect(ip)
        topicName=zoneTopic.get().strip()
        if len(topicName) == 0:
            return
        client.loop_start()
        client.subscribe(topicName)
        message = zoneMessage.get().strip()
        if len(message) == 0:
            return
        if len(message) > 1000:
            return
        client.publish(topicName, message)
        client.on_message=on_message
        zoneMessage.delete(0, "end")
        errorLabel.config(text="")
    except OSError as e:
        errorLabel.config(text=e)

root=tk.Tk()
root.geometry("575x470")
root.title("JustMQTT")
root.resizable(False, False)
root.config(bg='#171717')

titleLabel=tk.Label(root, text="JustMQTT", font="size 14 underline", fg="#caf")
titleLabel.grid(column=0, row=0, columnspan=3, pady=10)
titleLabel.config(bg='#171717')

usernameLabel=tk.Label(root, text="Username:", font="size 11", fg="#c3c3c3")
usernameLabel.grid(column=0, row=1, sticky='w', padx=5)
usernameLabel.config(bg='#171717')

zoneUsername=tk.Entry(root, width="15", font="size 12", bg="#373737", fg="#c3c3c3", border=0, disabledbackground="#272727")
zoneUsername.grid(column=1, row=1, sticky='w', padx=5, pady=5)

ipLabel=tk.Label(root, text="Broker IP:", font="size 11", fg="#c3c3c3")
ipLabel.grid(column=0, row=2, sticky='w', padx=5)
ipLabel.config(bg='#171717')

zoneIP=tk.Entry(root, width="15", font="size 12", bg="#373737", fg="#c3c3c3", border=0, disabledbackground="#272727")
zoneIP.grid(column=1, row=2, sticky='w', padx=5, pady=5)

buttonIP=tk.Button(root, text="Save", font="size 12", border=0, width=12, bg="#373737", fg="#c3c3c3", command=send_info)
buttonIP.grid(column=2, row=3, sticky='e', padx=5, pady=5)

topicLabel=tk.Label(root, text="Topic:", font="size 11", fg="#c3c3c3")
topicLabel.grid(column=0, row=4, sticky='w', padx=5)
topicLabel.config(bg='#171717')

zoneTopic=tk.Entry(root, width="30", font="size 12", bg="#373737", fg="#c3c3c3", border=0, state="disable", disabledbackground="#272727")
zoneTopic.grid(column=0, row=5, sticky='w', padx=5, pady=5)

buttonTopic=tk.Button(root, text="Subscribe", font="size 12", bg="#373737", fg="#c3c3c3", border=0, width=12, command=subscribe_topic, state="disable")
buttonTopic.grid(column=2, row=5, sticky='e', padx=5, pady=5)

enterMessageLabel=tk.Label(root, text="Enter your message:", font="size 11", fg="#c3c3c3")
enterMessageLabel.grid(column=0, row=6, sticky='w', padx=5)
enterMessageLabel.config(bg='#171717')

zoneMessage=tk.Entry(root, width="30", font="size 12", bg="#373737", fg="#c3c3c3", border=0, state="disable", disabledbackground="#272727")
zoneMessage.grid(column=0, row=7, sticky='w', padx=5, pady=5)

buttonSend=tk.Button(root, text="Send", font="size 12", bg="#373737", fg="#c3c3c3", border=0, width=12, command=publish_message, state="disable")
buttonSend.grid(column=2, row=7, sticky='e', padx=5, pady=5)

messageLabel=tk.Label(root, text="Messages:", font="size 11", fg="#c3c3c3")
messageLabel.grid(column=0, row=8, sticky='w', padx=5)
messageLabel.config(bg='#171717')

getMessageLabel=tk.Text(root, font="size 10", fg="#c3c3c3", height="5", state="disable", wrap="word")
getMessageLabel.grid(column=0, row=9, columnspan=3, sticky='w', padx=5, pady=5)
getMessageLabel.config(bg='#171717')

buttonClose=tk.Button(text="X", font="size 12", bg='#caf', fg="#171717", border=0, width=6, command=root.destroy)
buttonClose.grid(column=2, row=10, sticky='e', padx=5)

copyrightLabel=tk.Label(text="©seguinleo", font="size 8", fg="#c3c3c3")
copyrightLabel.grid(column=0, row=10, sticky='w', pady=10)
copyrightLabel.config(bg='#171717')

errorLabel=tk.Label(root, font="size 8", fg="#faa")
errorLabel.grid(column=0, row=11, pady=10, columnspan=3)
errorLabel.config(bg='#171717')

get_credentials()
root.mainloop()
