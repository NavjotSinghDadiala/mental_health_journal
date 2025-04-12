import time
import datetime
import threading
import os
from playsound import playsound

# Set your default device here
adb_device = "192.168.90.118"

contacts = {
     "sourabh": "+918369354802",
    "saurabh": "+918369354802",
    "siddhesh": "+919322049117",
    "aarti mam": "+919323134203",
    "sanjivani mam": "+918779672968",
    "anjum": "+917400410414",
    "yash": "+919372577073",
    "dad" : "8369126849",
}

def adb_command(cmd):
    full_cmd = f"adb -s {adb_device} {cmd}"
    print(f"Executing: {full_cmd}")
    os.system(full_cmd)

def schedule_call_with_audio(contact_name, audio_file_path, scheduled_time_str):
    contact_name = contact_name.lower()
    phone_number = contacts.get(contact_name)

    if not phone_number:
        print(f"Contact {contact_name} not found.")
        return

    try:
        # Parse the time string like '17:45'
        scheduled_time = datetime.datetime.strptime(scheduled_time_str, "%H:%M").time()

        def task():
            print(f"Waiting until {scheduled_time} to make the call to {contact_name}...")
            while True:
                now = datetime.datetime.now().time()
                if now >= scheduled_time:
                    break
                time.sleep(10)

            print(f"Calling {contact_name} at {phone_number}")
            adb_command(f'shell am start -a android.intent.action.CALL -d tel:{phone_number}')
            time.sleep(5)  # Wait for the call to connect

            print(f"Playing message: {audio_file_path}")
            playsound(audio_file_path)

        thread = threading.Thread(target=task)
        thread.start()
        return f"Scheduled a call to {contact_name} at {scheduled_time_str} with audio."
    
    except Exception as e:
        return f"Failed to schedule call: {str(e)}"
