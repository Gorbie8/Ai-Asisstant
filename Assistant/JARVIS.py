"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
IMPORTS -------------------------------------------------------------------------------------------------------------------------------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from Skills import get_date_and_time


import time
import audioop
import pyaudio
import wave
import speech_recognition
import playsound
import pyttsx


f = open('CONFIG.txt')
lines = f.readlines()
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
HOT WORD CONFIGURATION ----------------------------------------------------------------------------------------------------------------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
HOT_WORD_RECORD_SECONDS = float(lines[18])
HOT_WORD_AUDIO_OUTPUT_FILENAME = "Data\\hot_word_search.wav"
NOISE_THRESHOLD = int(lines[21])
ACTIVE_BLEEP = 'Data\\active_sound.mp3'
HOT_WORDS = (lines[24].replace("[", "").replace("]", "").replace(",", "").replace('"', "")).split()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ASSISTANT CONFIGURATION ---------------------------------------------------------------------------------------------------------------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
GENDER = int(lines[35])
if GENDER == 1:
    GENDER = "female"
elif GENDER == 2:
    GENDER = "male"

SPEED = int(lines[38])
VOLUME = int(lines[41])
COMMAND_RECORD_TIME = float(lines[44])
COMMAND_OUTPUT_FILENAME = "Data\\command.wav"


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PYAUDIO CONFIGURATION AND SETUP -------------------------------------------------------------------------------------------------------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# PyAudio Config
# Only change if you know what your doing
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
# PyAudio Stream
audio_data = pyaudio.PyAudio()
audio_stream = audio_data.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def sound_level():
    """
    Reads the noise level coming from a microphone
    Data ranges from 0 to 33000
    Ambient is around 1000 and talking is around 6000

    Returns: The noise level of the microphone in live time
    """
    for i in range(0, 2):
        data = audio_stream.read(CHUNK)
        if True:
            reading = audioop.max(data, 2)
        time.sleep(.0001)
        return reading


def record_audio(audio_output_filename, record_seconds):
    """
    Records audio and saves it as a WAV audio file
    1.5 Seconds is used if only looking for one word

    Receives: The output file name and the amount of seconds to record for
    """
    print "Recording..."
    frames = []
    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = audio_stream.read(CHUNK)
        frames.append(data)
    print "Finished recording"
    # stop Recording

    wavefile = wave.open(audio_output_filename, 'wb')
    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(audio_data.get_sample_size(FORMAT))
    wavefile.setframerate(RATE)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()


def setup_text_to_speech_engine(gender, speed, volume_percentage):
    engine = pyttsx.init()
    if gender == "female" or gender == "Female":
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    elif gender == "male" or gender == "Male":
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')

    engine.setProperty('rate', speed)

    volume = float(volume_percentage) / 100
    engine.setProperty('volume', volume)
    return engine


def speech_to_text(audio_output_filename):
    """
    Converts WAV files into speech, known as a STT or speech to text
    Uses the Google analyser, and returns the converted result with the highest confidence

    Receives: the audio filename to read from
    Returns: the output text
    """
    print "Analysing"
    analyser = speech_recognition.Recognizer()
    audio_file = speech_recognition.AudioFile(audio_output_filename)
    with audio_file as source:
        audio = analyser.record(source)
    return analyser.recognize_google(audio)


def hot_word_loop(audio_output_filename, record_seconds, hot_words):
    """
    1. Looks for noise over a threshold
    2. Records audio for set seconds
    3. Analysis's the audio and returns the stt
    4. Checks if the hot word was said or if a similar word was said
    5. Returns a positive if the hot word is said

    Receives: The audio output file name to record to
              The amount of time to record for
    Returns:  Whether the hot word was said

    """
    noise_level = sound_level()
    if noise_level > NOISE_THRESHOLD * 100:
        print "Threshold reached"
        record_audio(audio_output_filename, record_seconds)
        user_raw_output = speech_to_text(audio_output_filename)
        if user_raw_output is None:
            user_text_output = "No Text"
            hot_word_loop(audio_output_filename, record_seconds, hot_words)
        else:
            user_text_output = user_raw_output.lower()

        print user_text_output

        if any(x in user_text_output for x in hot_words):
            print "Hot word found"
            return True
        else:
            return False


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
SKILL WORD SEARCH ---------------------------------------------------------------------------------------------------------------------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def find_skill_words(user_command):

    found_word = "None"
    found_modifier = "None"
    command = user_command.split(" ")

    keywords = {"time": ["france", "spain", "united_states", "china", "italy", "mexico", "uk", "turkey", "germany", "thailand", "australia", "japan"],
                "date": ["france", "spain", "united_states", "china", "italy", "mexico", "uk", "turkey", "germany", "thailand", "australia", "japan"]
                }

    for i in keywords:
        for x in command:
            if x == i:
                found_word = i
                modifiers = keywords[found_word]
                for y in modifiers:
                    for t in command:
                        if y == t:
                            found_modifier = t

    return found_word, found_modifier


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PROGRAM START -------------------------------------------------------------------------------------------------------------------------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
while True:
    tts_engine = setup_text_to_speech_engine(GENDER, SPEED, VOLUME)
    hot_word_found = hot_word_loop(HOT_WORD_AUDIO_OUTPUT_FILENAME, HOT_WORD_RECORD_SECONDS, HOT_WORDS)
    if hot_word_found is True:
        playsound.playsound(ACTIVE_BLEEP)
        record_audio(COMMAND_OUTPUT_FILENAME, COMMAND_RECORD_TIME)
        user_command_raw = speech_to_text(COMMAND_OUTPUT_FILENAME)

        if type(user_command_raw) is unicode:
            print user_command_raw
            keyword, modifier = find_skill_words(str(user_command_raw.lower()))
            print keyword

            """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            ADD SKILLS HERE -----------------------------------------------------------
            """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            if keyword == "time":
                tts_engine.say(get_date_and_time.time_or_date_in_place(modifier, True, False))
                tts_engine.runAndWait()
            elif keyword == "date":
                tts_engine.say(get_date_and_time.time_or_date_in_place(modifier, False, True))
                tts_engine.runAndWait()

            print keyword
            print modifier
        else:
            pass
