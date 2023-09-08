import speech_recognition as sr
import re
import pandas as pd  # for database management
import random        # for OTP generation
from word2number import w2n  # for converting words to numbers

# Function for converting speech to text
def speechtotext(time):  
    """
    Captures audio from the microphone and converts it to text using the Google Web Speech API.
    
    Args:
        time (int): The amount of time (in seconds) to record audio.
    
    Returns:
        str or None: The recognized text or None if recognition fails.
    """
    # Initializing the recognizer
    recognizer = sr.Recognizer()

    # Capturing audio from the microphone
    with sr.Microphone() as source:
        print("Say your input")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=time)  # Listen for up to 'time' seconds 

    # Use the recognizer to convert speech to text
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None  # Return None if speech couldn't be recognized
    except sr.RequestError as e:
        return None  # Return None if there's an issue with the request

# Function to convert words to numbers using 'word2number'
def wordtonum(text):
    """
    Converts spoken numbers (e.g., "fifty-one") to their numeric integer representation (e.g., 51).
    
    Args:
        text (str): The spoken number in text format.
    
    Returns:
        int or None: The numeric integer representation or None if conversion fails.
    """
    try:
        ind = w2n.word_to_num(text)  # Convert the word to a number
        print(type(ind))
    except ValueError as e:
        print(f"Error converting to numeric: {e}")

# Regular expressions for doctor types and days
doctor_types = r"physician|dermatologist|cardiologist|orthopedic|pediatrician|dentist"
day = r"monday|tuesday|wednesday|thursday|friday|saturday|sunday"


''''
Sample data to store appointment details for patient
data attributes
name: patient's name
doctor_type = which doctor patient wants to consult
day: day of appointment
time: time slot for appointment
available: availability for time slot (yes/no)
OTP: One  time password for appointment confirmation
'''
data = {
    "name": ["" for _ in range(60)],
    "doctor_type": ["physician"] * 10 + ['dermatologist'] * 10 + ['cardiologist'] * 10 + ['orthopedic'] * 10 + ['pediatrician'] * 10 + ['dentist'] * 10,
    "day": ((['monday'] * 2) + (['tuesday'] * 2) + (['wednesday'] * 2) + (['thursday'] * 2) + (['friday'] * 2)) * 6,
    "time": ["12:30 - 13:00", "13:00 - 13:30"] * 30,
    "available": ["yes"] * 60,
    "OTP": [0] * 60
}

data = pd.DataFrame(data)

class AppointmentBot:
    def __init__(self):
        self.doctor_types = doctor_types
        self.bot = "Bot:"
        self.day = day
        self.data = data
        self.greeting()

    def greeting(self):
        """
        Initiates a conversation with the user, starting with asking for their name.
        """
        self.details = {}
        print(self.bot, "Hi, this is the appointment booking chatbot. Please tell me your name.")
        name = speechtotext(5)
        print(self.bot, f"Hi {name.capitalize()}, please tell me about the doctor you are planning to visit.")
        self.details['name'] = name
        self.Doctor(name)

    def Doctor(self, name):
        """
        Asks the user about the type of doctor they want to visit.
        
        Args:
            name (str): The name of the user.

        """
        doctor = speechtotext(10).lower()
        if re.search(self.doctor_types, doctor):
            doctor_type = re.search(self.doctor_types, doctor).group()
            print(self.bot, f"Which day are you planning to visit the {doctor_type.capitalize()}?")
            self.details["doctor_type"] = doctor_type
            self.day_available(doctor_type)
        else:
            print(self.bot, "Sorry, I didn't understand your request. Please enter again.")
            self.Doctor(name)

    def day_available(self, doctor_type):
        """
        Asks the user about the available days for the selected doctor.
        
        Args:
            doctor_type (str): The type of doctor selected by the user.
        """
        day_slot = speechtotext(5).lower()
        if re.search(self.day, day_slot):
            day_slot = re.search(self.day, day_slot).group()
            print(self.bot, f"Slots available for {day_slot.capitalize()}.")
            self.details["day_slot"] = day_slot
            self.available_slots(day_slot)
        else:
            print(self.bot, "Sorry, I didn't understand your request. Please enter the details again.")
            self.day_available(doctor_type)

    def available_slots(self, day_slot):
        """
        Lists the available time slots for the selected day and asks the user to choose a slot.
        
        Args:
            day_slot (str): The selected day.
        """
        slot = (self.data.loc[self.data['day'] == day_slot])
        slot = slot.loc[slot['available'] == 'yes']
        slot = slot.loc[slot['doctor_type'] == self.details['doctor_type']]
        print(slot['time'])
        print(self.bot, "Please enter only the time slot number.")

        # ind = speechtotext(4)
        # ind = wordtonum(ind)
        ind = int(input())


        if ind is None:
            self.available_slots(day_slot)

        self.data.iloc[ind, self.data.columns.get_loc('available')] = 'no'
        slot = (self.data.iloc[ind])['time']
        self.details["slot"] = slot
        print(f"Your appointment with the {self.details['doctor_type'].capitalize()} is scheduled.")
        self.finish()

    def finish(self):
        """
        Generates an OTP for the appointment and displays it to the user.
        """
        OTP = random.randint(1000, 9999)
        print(f"Your OTP for the appointment is {OTP}.")
        self.details["OTP"] = OTP
        self.print_details()

    def print_details(self):
        """
        Prints the appointment details to the user.
        """
        print("Your appointment details are as follows:")
        for key, value in self.details.items():
            print(key.capitalize(), value)

# Create an instance of the AppointmentBot class
bot = AppointmentBot()
