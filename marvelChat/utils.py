import csv
import random
import speech_recognition as sr
import pyttsx3;


context = [None, None]
super_heroes = []
with open('marvel_chars.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    if row[2].strip() == "":
      continue
    if "(" in row[0]:
      super_heroes.append((row[0][:row[0].index("(")].strip().lower(), int(row[1]), row[2].strip()))
      super_heroes.append((row[0][row[0].index("(") + 1:-1].strip().lower(), int(row[1]), row[2].strip()))
    else:
      super_heroes.append((row[0].strip().lower(), int(row[1]), row[2].strip()))


def get_good_heroes(score):
  valid = []
  for hero, power, story in super_heroes:
    if power > score:
      valid.append(hero)
  return random.choice(valid)

def get_bad_heroes(score):
  valid = []
  for hero, power, story in super_heroes:
    if power < score:
      valid.append(hero)
  return random.choice(valid)

def match_superheros(text):
  for hero, power, story in super_heroes:
    # print(hero)
    if hero in text:
      return True, (hero, power, story)
  return False, None


def match_aff(text):
  for match in ["yee", "yes", "go ahead", "ya"]:
    if match in text:
      return True, True
  for match in ["no", "nah", "do not", "stop", "don't want"]:
    if match in text:
      return True, False
  return False, False

def match_pronoun(text):
  for match in [" he ", " she ", " they ", "them", "him", "her"]:
    if match in text + " ":
      return True, None
  return False, None

def match_power(text):
  for match in ["powerful", "power", "strong"]:
    if match in text:
      return True, None
  return False, None


def match_rank(text):
  for match in ["is anyone", "anybody", "am i more", "am i less", "am i as"]:
    if match in text:
      return True, None
  return False, None


def match_who(text):
  for match in ["who", "describe", "tell me about", "about"]:
    if match in text:
      return True, None
  return False, None


def match_me(text):
  for match in ["me", "i"]:
    if match in text:
      return True, None
  return False, None

def match_greeting(text):
  for greeting in ["hello", "hi", "how are you", "hey", "heyo"]:
    if greeting in text:
      return True, None
  return False, None


def match_bye(text):
  for bye in ["bye", "good bye", "see you", "shut up", "stop"]:
    if bye in text:
      return True, None
  return False, None


def respond(text, my_power, my_name):
  if (context[0] is not None) and match_aff(text)[0]:
    _, detail = match_aff(text)
    context[0] = None
    if detail is True:
      return "Great! I'll update the settings. Thanks for being a hero."
    else:
      return "That's sad to hear. Maybe next time!"

  context[0] = None

  if (context[1] is not None) and match_pronoun(text)[0]:
    hero, power, story = context[1]
    hero = hero[0].upper() + hero[1:]
    match2, _ = match_who(text)
    match3, _ = match_power(text)
    if match2:
      return story
    if match3:
      if my_power > power:
        return "You're more powerful than " + hero + "!" \
            " " + hero + " has nothing on your planet-saving powers."
      elif my_power < power:
        return hero + " is still more powerful than you." \
            " " + hero + "'s " + str(power) + " power points tower over your " \
            "mere " + str(my_power) + "."
      return "Wow, you two are perfectly matched."

  match, details = match_superheros(text)
  if match:
    hero, power, story = details
    context[1] = details
    hero = hero[0].upper() + hero[1:]
    match2, _ = match_who(text)
    if match2:
      return story
    if my_power > power:
      return "You're more powerful than " + hero + "!" \
          " " + hero + " has nothing on your planet-saving powers."
    elif my_power < power:
      return hero + " is still more powerful than you." \
          " " + hero + "'s " + str(power) + " power points tower over your " \
          "mere " + str(my_power) + "."
    return "Wow, you two are perfectly matched."

  context[1] = None

  match, _ = match_power(text)
  if match:
    match2, _ = match_rank(text)
    if match2:
      return "At " + str(my_power) + " points, you're more powerful " \
          "than " + get_bad_heroes(my_power) + " and less powerful than" \
          " " + get_good_heroes(my_power) + "."
    else:
      context[0] = True
      return "You are at " + str(my_power) + ". Gain more power by" \
          " saving more power! Want to extend your temperature " \
          "range?"

  match, _ = match_greeting(text)
  if match:
    return "Hi " + my_name + "."
  match, _ = match_bye(text)
  if match:
    return "Bye " + my_name + "."
  return "?"


def handle(inp):
  inp = str(inp).strip().lower()
  return respond(inp, 1000, "Eric")


def voice():
  engine = pyttsx3.init();
  r = sr.Recognizer()
  with sr.Microphone() as source:
    audio = r.listen(source)
    # recognize speech using Microsoft Bing Voice Recognition
    BING_KEY = "42cfbf81a1894b8fab2c197e9b509bb4"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
    try:
      text = r.recognize_bing(audio, key=BING_KEY)
      print("You: ", text)
      response = handle(text)
      print(response)
      engine.say(response)
      engine.runAndWait()
    except sr.UnknownValueError:
      print("We can't hear you, can you speak louder?")
    except sr.RequestError as e:
      print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

def text():
  text = input("You: ")
  response = handle(text)
  print(response)

if __name__ == "__main__":
  print("Say something!")
  while True:
    voice()

