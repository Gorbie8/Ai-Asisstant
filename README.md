# Ai-Asisstant
Customisable Ai assistant using Python 2

### Usage
Use the steps below to customise the assistant. You can customise the hotword, gender, and speed. Then run the script to turn the assistant on.

### How It Works
- When sound is detected above the threshold it will start a by default 1.5 second sound recording using PyAudio
- That sound clip will be then analysed by the speech recognition library by Anthony Zhang
- If any of the words analysed match with the hot words a bleep will play and another by default 3-second clip will be recorded
- If any of the words analysed match any of the keywords and or any of the modifier words they will activate there dedicated skill function
- The assistant will then respond using the google text to speech engine

# Customising

### Configuring
Edit the CONFIG file to change the personality of the assistant. You can change the timing involved with recording commands and the activate word. You can have multiple hot words as sometimes words that sound similar will be picked up instead of the actual hotword. The assistant has multiple factors that can be set such as gender, talking speed and volume. Ensure you only change the value on the line its originally on and don't input values outside the scopes. 

### Creating Skills
1. A skill file can have multiple functions inside it
2. The function can have a modifier argument or not
3. The function can have other arguments as well
4. It should return what should be said by the assistant in the form of a string
##### Example
```
def tell_joke(modifier):
    if modifier == "funny":
        return "I ate a clock yesterday, it was very time consuming."
    elif modifier == "pun":
        return "What do you call a fake noodle? An Impasta."
```

### Adding Skills
1. Import the skill using **from Skills import (skill name)** at the top
2. Above PROGRAM START where it says **SKILL WORD SEARCH** you will need to add the keyword as a dictionary and a list of the modifier words in the dictionary. See the example below
3. Near the bottom of the script where it says **ADD SKILLS HERE**, you need to add another elif statement defining what keyword is needed. In the elif use **tts_engine.say(skill_file_name.skill_name(modifier))**. Then underneath **tts_engine.runAndWait()**. Follow example below.
##### Example 1
```
from Skills import joke
```
##### Example 2
```
keywords = {"time": ["france", "spain", "mexico", "uk", "turkey", "germany", "thailand", "australia", "japan"],
            "joke": ["funny", "pun"]
           }
```
##### Example 3
```
if keyword == "time":
        tts_engine.say(get_date_and_time.time_or_date_in_place(modifier, True, False))
        tts_engine.runAndWait()
elif keyword == "joke":
        tts_engine.say(joke.tell_joke(modifier))
        tts_engine.runAndWait()
```
