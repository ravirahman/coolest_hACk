import csv


super_heroes = []
with open('temp.csv', 'r') as f:
  reader = csv.reader(f)
  for row in reader:
    super_heroes.append((row[0], int(row[1]), row[2]))


def match_superheros(text):
  for hero, power, story in super_heroes:
    if hero in text:
      return True, (hero, power, story)
  return False, None


def match_power(text):
  for match in ["powerful", "power", "strong"]:
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
          "mere " + str(my_power) + " existence."
    return "Wow, you two are perfectly matched."
  match, _ = match_power(text)
  if match:
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
  while True:
    print(handle(input("You: ")))

