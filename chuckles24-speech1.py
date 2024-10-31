import os
from openai import AzureOpenAI

# Create an instance of the AzureOpenAI class with your Azure API credentials
client = AzureOpenAI(azure_endpoint="[YOUR AI ENDPOINT HERE]",
api_version="[YOUR AI API VERSION HERE]",
api_key="[YOUR AI API KEY HERE]")

import azure.cognitiveservices.speech as speechsdk
# Creates an instance of a speech config with specified subscription key and service region.
speech_key = "[YOUR KEY HERE]"
service_region = "[AZURE REGION HERE]"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.endpoint_id = "[YOUR SPEECH API ENDPOINT HERE]"
speech_config.speech_synthesis_voice_name = "[YOUR SPEECH VOICE NAME HERE]"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Import the required modules
import sys
import time
import random
import speech_recognition as sr
import gpiod

#Configure access to GPIO stuff.
chip = gpiod.Chip('gpiochip4')

#set up rock pin...  GPIO 14 is where I have the relay connected to the RPi that turns the motor on and off.
rock_pin = 14
rock_line = chip.get_line(rock_pin)
rock_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

# Create an instance of the Recognizer class 
speech_config = speechsdk.SpeechConfig(subscription="[YOUR AZURE SUB ID HERE]", region="[YOUR AZURE REGION HERE")
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

# Function to get input from the microphone
def from_mic():
    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    print(speech_recognition_result.text)
    # If the speech recognition result is empty, keep listening until a valid result is obtained
    while speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        speech_recognition_result = speech_recognizer.recognize_once_async().get()
    return speech_recognition_result.text

# take as input a string and say it.  aLso turn on the rock line to indicate that the prop is speaking.
def sayit(s):
        rock_line.set_value(1)
        result = speech_synthesizer.speak_text_async(s).get()
        time.sleep(1)
        rock_line.set_value(0)

# Function to send a message to the OpenAI chatbot model and return its response
def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = client.chat.completions.create(model="gpt-4o",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=1000,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,  
        temperature=0.7)            # The stopping sequence for the generated response, if any (not used here)

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text
    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

# Main function that runs the chatbot
def main():
    # Initialize the conversation history with a message from the chatbot
    message_log = [
        {"role": "system", "content": "You are a silly yet evil clown Halloween prop.  Your name is Chuckles.  You respond to questions in a silly yet evil way.  Do not respond with emojis or any special characters please.  And do not respond with laughter.  Responses should be angry and short.  Also you have little green frogs for hands and are very sensitive about them.  You do not have any feet and this also bothers you a great deal."}
    ]

    # Set a flag to keep track of whether this is the first request in the conversation
    first_request = True

    # Start a loop that runs until the user says "quit"
    while True:
        if first_request:
            # If this is the first request, get the user's input and add it to the conversation history
            # Use the microphone as source for input
            print("Listening...")
            user_input = from_mic()

            message_log.append({"role": "user", "content": user_input})
            # Send the conversation history to the chatbot and get its response
            response = send_message(message_log)
            #say the response
            sayit(response)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})
            # Set the flag to False so that this branch is not executed again
            first_request = False

        else:
            # If this is not the first request, get the user's input and add it to the conversation history
            # If this is the first request, get the user's input and add it to the conversation history
            print("Listening...")
            user_input = from_mic()
            # If the user says "quit", end the loop and print a goodbye message
            if user_input.lower() == "quit.":
                print("Goodbye!")
                break
            message_log.append({"role": "user", "content": user_input})
            # Send the conversation history to the chatbot and get its response
            response = send_message(message_log)
 
            #say the response
            sayit(response)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})

# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()

