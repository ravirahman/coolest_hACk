import csv
import random
import speech_recognition as sr


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


def match_power(text):
  for match in ["powerful", "power", "strong"]:
    if match in text:
      return True, None
  return False, None


def match_rank(text):
  for match in ["is anyone", "anybody", "am i"]:
    if match in text:
      return True, None
  return False, None


def match_who(text):
  for match in ["who", "describe", "tell me about", "about"]:
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
  match, details = match_superheros(text)
  if match:
    hero, power, story = details
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
  match, _ = match_power(text)
  if match:
    match2, _ = match_rank(text)
    if match2:
      return "At " + str(my_power) + " points, you're more powerful " \
          "than " + get_bad_heroes(my_power) + " and less powerful than" \
          " " + get_good_heroes(my_power) + "."
    else:
      return "Your power score is " + str(my_power) + ". Gain more power by" \
          " saving more power! Want to extend your comfortable temperature " \
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
  return respond(inp, 15, "Eric")


if __name__ == "__main__":
  print("Hey")
  while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
      print("Say something!")
      audio = r.listen(source)
			# recognize speech using Microsoft Bing Voice Recognition
			BING_KEY = "42cfbf81a1894b8fab2c197e9b509bb4"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
			try:
        text = r.recognize_bing(audio, key=BING_KEY)
			except sr.UnknownValueError:
				print("We can't hear you, can you speak louder?")
				continue
			except sr.RequestError as e:
				print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
			  return
			print("You: ", text)
			response = handle(text)
			print(response)
			speech.say(response)

