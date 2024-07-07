# Doctor_appointment_chatbot
Here is the code for a simple appointment booking chat which which performs basic data preprocessing on the input and return the suitable output. For data storing pandas is used and speech recognition api is used for converting speed data to text.

Chatbot Domain: Appointment Booking

Description:

The Appointment Booking Chatbot is a conversational agent designed to assist users in scheduling medical appointments with different types of doctors. It offers a user-friendly interface through speech recognition, allowing users to interact with the chatbot using their voice. This chatbot operates within the domain of medical appointments and provides the following functionality


Usage:

User Introduction: The chatbot starts by introducing itself and asks for the user's name.

Doctor Selection: Users can specify the type of doctor they wish to consult (e.g., physician, dermatologist, cardiologist, etc.).

Day Selection: Users can choose the day on which they want to schedule the appointment (e.g., Monday, Tuesday, etc.).

Time Slot Selection: The chatbot lists available time slots for the selected day and doctor type. Users can choose a convenient time slot.

Appointment Confirmation: Once a time slot is selected, the chatbot confirms the appointment and generates a One-Time Password (OTP) for verification.

OTP Verification: The OTP is provided to the user, and it will be required at the time of the actual appointment.

Domain:

The chatbot operates primarily within the domain of medical appointments. Users can ask questions and interact with the chatbot to schedule appointments with various types of doctors, inquire about available days and time slots, and receive appointment confirmations.


Improvements:

This bot is hard coded and designed for only appointment booking purposes. Can help bot learn from the training data to improve user experience

Using natural language libraries like nltk can optimize the text bot for introduction and slot booking inputs like "My name is Dewansh", or "book fifty fifth slot for me" in inputs where we assumed single word string or integer input.
