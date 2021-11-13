import json, sys, datetime, time, random, imdb

appInfo = {
  "Name": "Show List",
  "Creator": "Mark E",
  "Version": "1.2",
  "Description": "A program that allows you to keep track of shows you're watching."
}

showsToWatch = []
showWatching = [{"Name": "None", "Episode": 1, "Status": "None"}]
completedShows = []
name = "None"
assistantName = "Clover"
increment = 0
ia = imdb.IMDb()
selectedSearchedShow = None # Going to be used temporarily.

def completed():
  global completedShows
  if not completedShows:
    input(f"[{assistantName}] 😅 < You haven't completed any shows yet! Try completing some shows first.")
  else:
    heading("Menu > Completed Shows")
    for title in completedShows:
      print(f"-> {title}")
    print("[i] Total items: " + str(len(completedShows)))
    input("Press ENTER to exit. | ")

def loopThroughShows():
  global showWatching, increment

  increment = 0

  print("----------------------------------------------")
  for i in range(len(showWatching)):
    print(f"[{i}] | Show: {showWatching[i]['Name']} | EP: {showWatching[i]['Episode']} | Status: {showWatching[i]['Status']}")
  print("----------------------------------------------")

def checkShow(show):
  global showWatching, showsToWatch

  for i in range(len(showsToWatch)):
    if showsToWatch[i]["Name"] == show:
      input(f"[{assistantName}] 😅 < Haha, you're already planning on watching this show!")
      return True
  
  for i in range(len(showWatching)):
    if showWatching[i]["Name"] == show:
      input(f"[{assistantName}] 😅 < Haha, you're already watching watching that show! Try again!")
      return True
  return False

def addNewShow(show, episode: int, location=None):
  global showWatching, showsToWatch, selectedSearchedShow

  
  if location == "watchingNow":
    if showWatching[0]["Name"] == "None":
      showWatching[0]["Name"] = show
      showWatching[0]["Episode"] = episode
      showWatching[0]["Status"] = "Watching"
    else:
      showWatching.append({"Name": show, "Episode": episode, "Status": "Watching"})
  elif location == "watchingLater":
    showsToWatch.append({"Name": show, "Episode": episode})
  elif location == "both":
    if showWatching[0]["Name"] == "None":
      showWatching[0]["Name"] = show
      showWatching[0]["Episode"] = episode
    else:
      showWatching.append({"Name": show, "Episode": episode, "Status": "Watching"})
    showsToWatch.append({"Name": show, "Episode": episode})
  json.dump((name, showsToWatch, showWatching, completedShows), open("data.py", "w"), indent=2)
  

def showData(show, item="all"):
  try:
    if item == "all":
      return (
      f"-> SHOW: {show.data['title']}\n"
      f"-> RATING: {str(show.data['rating'])} / 10.0\n"
      f"-> GENRES: {show.data['genres']}\n"
      f"-> YEARS ACTIVE: {show.data['series years']}\n"
      f"-> VOTES: {str(show.data['votes'])}\n"
      f"-> ABOUT: {show.data['plot'][0]}"
    )
    elif item == "title":
      return show.data['title']
    elif item == "year":
      return show.data['year']
    elif item == "rating":
      return str(show.data['rating'])
    elif item == "votes":
      return str(show.data['votes'])
    elif item == "genres":
      return show.data['genres']
    elif item == "plot":
      return show.data['plot'][0]
    elif item == "episodes":
      return ia.get_movie_episodes(show.movieID)["data"]["number of episodes"]
  except:
    return "[X] Something went wrong. Please contact [MARK] if you think there is a bug."

def findShow(show):
  global showsToWatch, showWatching, completedShows, name, assistantName, selectedSearchedShow
  search = ia.search_movie(show)
  if search:
    for i in range(len(search)):
      print(f"[{i}] | {search[i]['long imdb canonical title']}")
    show = input(f"[{assistantName}] 🤔 < Which show would you like to view? (e to exit, otherwise enter the number of the show)")
    if show.strip().lower() == "e":
      return
    else:
      while True:
        try:
          show = int(show)
          break
        except:
          input(f"[{assistantName}] 😅 < Please enter a valid number.")
          show = input(f"[{assistantName}] 🤔 < Which show would you like to view? (e to exit, otherwise enter the number of the show)")
    showTitle = ia.get_movie(search[show].movieID)
    heading("SHOW INFO")
    print(showData(showTitle, "episodes"))
    selectedSearchedShow = str(showTitle)
    return True
  return False

def heading(text):
  for i in range(len(text)):
    print("-", end="")
  print()
  print(text)
  for i in range(len(text)):
    print("-", end="")
  print()

def create_name():
  global name
  input(f"[???] 👋😃 < Hello there! Welcome to this program. I believe this is our first time meeting, I'm {assistantName}!")
  input(f"[{assistantName}] 😄 < I will be your assistant while you're navigating in this program. Please ask me if you need any help!")
  input(f"[{assistantName}] 😟 < Oh, I'm sorry! I got caught up introducing myself... What is your name friend?")
  name = str(input("[...] 🤔 Please enter your name (The name entered will only be used for one thing, which involves time.): "))
  while True:
    confirm = input(f"[?] 🧐 {name.capitalize()}, so this is what you want me to call you? (y/n)")
    if confirm.strip().lower() == "y":
      break
    name = str(input("[...] 🤔 Please enter your name (The name entered will only be used for one thing, which involves time.): "))
  name = name.capitalize()
  json.dump((name, showsToWatch, showWatching, completedShows), open("data.py", "w"), indent=2)
  print(f"[{assistantName}] 😊 < Thank you for your time, {name}! You will now be redirected in a few seconds, please enjoy your time here!")
  time.sleep(random.randint(1, 3))
  return name
  

def check_time(name):
  now = datetime.datetime.now()

  if now.time() >= datetime.time(0) and now.time() <= datetime.time(11):
    print(f"[🌅] Good Morning, {name}.")
  elif now.time() >= datetime.time(12) and now.time() <= datetime.time(13):
    print(f"[🔆] Hello, {name}, it's Noon.")
  elif now.time() >= datetime.time(14) and now.time() <= datetime.time(18):
    print(f"[🌇] Good Afternoon, {name}.")
  elif now.time() >= datetime.time(19) and now.time() <= datetime.time(23):
    print(f"[🌙] Good Evening, {name}.")
  else:
    print(f"[👋] Hello, {name}, nice to see you.")

def listOfShows():
  global showsToWatch
  sys.stdout.write("[🔄] Fetching list...")
  sys.stdout.flush()
  sys.stdout.write("\r")
  sys.stdout.flush()
  if not showsToWatch:
    input("[X] Your list is empty! Go search for some shows to watch, then come here.")
  else:
    heading("Menu > Shows to Watch")
    for title in range(len(showsToWatch)):
      print(f"[->] {showsToWatch[title]['Name']} | EP: {showsToWatch[title]['Episode']}")
    print("[i] Total items: " + str(len(showsToWatch)))
    print("| View [title name (case sensitive)] | Exit [e]")
    action = str(input(">>> "))
    if action.strip().lower() == "e":
      return
    else:
      print("[🔄] Fetching show information...")
      for title in range(len(showsToWatch)):
        if showsToWatch[title]['Name'] == action.strip():
          heading("VIEW SHOW")
          movie_id = ia.search_movie(action.strip())[0].movieID # Search the show, get the first result, and get the movie ID.
          selected_show = ia.get_movie(movie_id) # Fetch the movie using the movie ID.
          print(showData(selected_show))
          return input("Press ENTER to exit. | ")
      input(f"[{assistantName}] 😅 < That show isn't in your list! Try again!")
      

def about():
  global appInfo
  heading("Menu > App Information")
  print(
    f"-> Program Name: {appInfo['Name']}\n"
    f"-> Program Creator: {appInfo['Creator']}\n"
    f"-> Program Version: {appInfo['Version']}\n"
    f"-> Program Description: {appInfo['Description']}\n"
  )
  input("Press ENTER to exit. | ")

def watching():
  global showWatching
  heading("Menu > Currently Watching")
  for i in range(len(showWatching)):
    print(f"| Show: {showWatching[i]['Name']} | EP: {str(showWatching[i]['Episode'])} | Status: {str(showWatching[i]['Status'])}")
  print("[i] Total items: " + str(len(showWatching)))
  print("| Change [c] | Remove [r] | Move to Completed [m] | Exit [e]")
  action = str(input(">>> "))
  if action == "c":
    change = str(input(f"[{assistantName}] 🤔 < Change what? (name/episode) "))
    if change.strip().lower() == "name":
      loopThroughShows()
      edit = input(f"[{assistantName}] 🤔 < Which show do you want to edit? ")
      try:
        edit = int(edit)
      except ValueError:
        input("[X] Invalid input, please try again!")
      if edit in range(0, len(showWatching)):
        title = str(input(f"[{assistantName}] 🧐 < What is the name of the show you're watching? ('e' to exit) "))
        if title.strip().lower() == "e":
          return
        if checkShow(title):
          return
        while True:
          update = str(input(f"[{assistantName}] 🙂 < You're currently watching '{title}'? (y/n) "))
          if update.strip().lower() == "y":
            break
          title = str(input(f"[{assistantName}] 🧐 < What is the name of the show you're watching? ('e' to exit) "))
          if title.strip().lower() == "e":
            return
        showWatching[edit]["Name"] = title
      else:
        return input("[X] Invalid number range.")
      input("[✔] Process complete.")
    elif change.strip().lower() == "episode":
      loopThroughShows()
      edit = input(f"[{assistantName}] 🤔 < Which show do you want to edit? ")
      try:
        edit = int(edit)
      except ValueError:
        input("[X] Invalid input, please try again!")
      if edit in range(0, len(showWatching)):
        episode = input(f"[{assistantName}] 🙂 < Please enter the episode number ('e' to exit). ")
        if episode.strip().lower() == "e":
          return
        try:
          episode = int(episode)
        except ValueError:
          input("[X] Invalid input, please try again!")
        while True:
          confirm = str(input(f"[{assistantName}] 🤔 < You're currently on episode {episode} on '{showWatching[edit]['Name']}'? (y/n)"))
          if confirm.strip().lower() == "y":
            break
          episode = input(f"[{assistantName}] 🙂 < Please enter the episode number ('e' to exit). ")
          if episode.strip().lower() == "e":
            return
          try:
            episode = int(episode)
          except ValueError:
            input("[X] Invalid input, please try again!")
        showWatching[edit]["Episode"] = episode
        if showWatching[edit]["Episode"] == showData(ia.search_movie(showWatching[edit]["Name"])[0], "episodes"):
          showWatching[edit]["Status"] = "Complete"
          return input(f"[✔] You've completed '{showWatching[edit]['Name']}'! Its status is now set to 'complete'.")
      else:
        return input("[X] Invalid number range.")
      input("[✔] Process complete.")
  elif action == "r":
    heading("Menu > Currently Watching > Remove Show")
    loopThroughShows()
    remove = input(f"[{assistantName}] 🤔 < Which show do you want to remove? ")
    try:
      remove = int(remove)
    except ValueError:
      input("[X] Invalid input, please try again!")
    confirm = str(input(f"[{assistantName}] 🤔 < Are you sure you want to remove {showWatching[remove]['Name']}? (y/n) "))
    if confirm.strip().lower() == "y":
      showWatching[remove]["Name"], showWatching[remove]["Episode"], showWatching[remove]["Status"] = "None", 1, "None"
      input("[✔] Removed show.")
    else:
      return
  elif action == "m":
    heading("Menu > Currently Watching > Move Show")
    loopThroughShows()
    move = input(f"[{assistantName}] 🤔 < Which show do you want to move? (e to exit): ")
    if move.strip().lower() == "e":
      return
    else:
      try:
        move = int(move)
      except ValueError:
        input("[X] Invalid input, please try again!")
      if showWatching[move]["Status"] == "Watching":
        confirm = str(input(f"[{assistantName}] 🤔 < You aren't completed with '{showWatching[move]['Name']}' yet, do you still want to move it to your list of completed shows? (y/n) "))
        if confirm.strip().lower() == "y":
          completedShows.append(showWatching[move]["Name"])
          showWatching.pop(move)
          input(f"[✔] Nice, you finished a show!")
      elif showWatching[move]["Status"] == "Complete":
        confirm = str(input(f"[{assistantName}] 🧐 < You've completed '{showWatching[move]['Name']}'! Do you want to move this show to your list of completed shows? (y/n) "))
        if confirm.strip().lower() == "y":
          completedShows.append(showWatching[move]["Name"])
          showWatching.pop(move)
          input(f"[✔] Nice, you finished a show!")
  else:
    return
  json.dump((name, showsToWatch, showWatching, completedShows), open("data.py", "w"), indent=2)
    

def userSettings():
  global name, showsToWatch, showWatching, completedShows
  heading("Menu > Settings")
  print(
    f"[{assistantName}] 🤔 What are you looking to change, {name}?\n"
    "[1] Change name.\n"
    "[2] Erase Data.\n"
    "[3] Exit."
  )
  settings = input(">>> ")
  try:
    settings = int(settings)
  except ValueError:
    input("[X] Invalid input, please try again!")
  if settings == 1:
    heading("Menu > Settings > Change Name")
    input(f"[{assistantName}] 🙂 < Oh? You want me to call you something else? Sure! What'll it be?")
    name = str(input("> Enter your new name: "))
    while True:
      confirm = input(f"[?] 🧐 {name.capitalize()}, so this is what you want me to call you? (y/n)")
      if confirm.strip().lower() == "y":
        break
      name = str(input("> Enter your new name: "))
    name = name.capitalize()
    json.dump((name, showsToWatch, showWatching, completedShows), open("data.py", "w"), indent=2)
    input(f"[{assistantName}] 😁 < Great, process complete, hello {name}!")


  elif settings == 2:
    heading("Menu > Settings > Erase Data")
    input(f"[{assistantName}] 😨 < Wha- You want to erase your data?! Why?!")
    input(f"[{assistantName}] 😔 < No no, I'm sorry. This must be something you're deciding on your own.")
    input(f"[{assistantName}] 😥 < You do know what this means right? All the shows you added will be GONE, for GOOD! I will also not remember you, {name}...")
    input(f"[{assistantName}] 😟 < Though, if you've come here, I'm sure you know. However, this is your choice, so I will not interfere with anything.")
    input(f"[{assistantName}] 😕 < So... what'll it be, {name}?")
    erase = input(
      "[!] By erasing your data, your name, list of shows, and what your currently watching will be wiped. Are you sure you want to continue?\n"
      "[1] Erase.\n"
      "[2] On second thought...\n"
      ">>> "
      )
    try:
      erase = int(erase)
    except ValueError:
      input("[X] Invalid input, please try again!")
    if erase == 1:
      confirm = str(input("[!!!] Final warning: Are you positive that you want to erase ALL data completely? This cannot be undone. (y/n)"))
      if confirm.strip().lower() == "y":
        input(f"[{assistantName}] 😔 < Well... it was nice meeting you, {name}. I guess this is where we part ways.")
        input(f"[{assistantName}] 😁 < Thank you for using Show List, goodbye.")
        name, showsToWatch, showWatching, completedShows = "None", [], [{"Name": "None", "Episode": 1, "Status": "None"}], []
        json.dump((name, showsToWatch, showWatching, completedShows), open("data.py", "w"), indent=2)
        input("[✔] Data erased successfully.")
        advance = str(input("[.] In order to continue using this program, you'll need to come up with a new name. If you want to later, type 'exit', if you want to now, type 'new'. (new/exit) "))
        if advance.strip().lower() == "new":
          create_name()
        else:
          sys.exit("[✔] Closed.")

def searchShows():
  global selectedSearchedShow
  heading("Menu > Search")
  show = str(input(f"[{assistantName}] 🧐 < What is the show you want me to find? (e to exit) "))
  if show.strip().lower() == "e":
    return
  print(f"[{assistantName}] 🤔 < Let me search for the show you're looking for, {name}!")
  if not findShow(show):
    input(f"[{assistantName}] 😔 < Sorry, Couldn't find your show. >>")
  else:
    print("| Add [a] | Search Again [s] | Exit [e]")
    action = str(input(">>> "))
    if action.strip().lower() == "a":
      if checkShow(selectedSearchedShow):
        return
      episode = int(input(f"[{assistantName}] 🤔 < Which episode would you like to watch?"))
      location = str(input(f"[{assistantName}] 🤔 < Where would you like to save this to? (watchingNow/watchingLater/both) "))

      saveLocation = "None"

      while location.strip().lower() not in ["watchingnow", "watchinglater", "both"]:
        input(f"[{assistantName}] 😕 < Sorry, I didn't understand that. >>")
        location = str(input(f"[{assistantName}] 🤔 < Where would you like to save this to? (watchingNow/watchingLater/both) "))
      if location.strip().lower() == "watchingnow":
        saveLocation = "watchingNow"
      elif location.strip().lower() == "watchinglater":
        saveLocation = "watchingLater"
      elif location.strip().lower() == "both":
        saveLocation = "both"
      addNewShow(selectedSearchedShow, episode, saveLocation)
      selectedSearchedShow = None
      print(f"[{assistantName}] 😄 < All done! >>")
    elif action.strip().lower() == "s":
      searchShows()
      return

def cloverGreeting():
  greetings = [
    f"Hello, {name}! 👋",
    f"Hey, {name}! 👋",
    f"Hi, {name}! 👋",
    f"Hey there, {name}! 👋",
    f"Welcome, {name}! 👋",
    f"Hiya, {name}! 👋",
    f"What's up, {name}? 👋",
  ]
  return random.choice(greetings)

def main():
  global showWatching, name, showsToWatch, completedShows, selectedSearchedShow

  try:
    name, showsToWatch, showWatching, completedShows = json.load(open("data.py", "r"))
  except:
    print("[.] Some data didn't load.")

  if name == "None":
    create_name()
  heading("Menu")
  check_time(name)
  while True:
    print(
      "------------------------------------------\n"
      f"[{assistantName}] 😄 < {cloverGreeting()}\n"
      "[1] View your list of upcoming shows.\n"
      "[2] View what you're currently watching.\n"
      "[3] View completed shows.\n"
      "[4] Search Show. [NEW!]\n"
      "[5] About the Program.\n"
      "[6] Settings.\n"
      "[7] Close.\n"
      "------------------------------------------"
    )
    action = input(">>> ")
    try:
      action = int(action)
    except ValueError:
      input("[X] Invalid input, please try again!")
    #match action:
      #case 1:
    if action == 1:
      listOfShows()
    #case 2:
    elif action == 2:
      watching()
    #case 3:
    elif action == 3:
      completed()
    #case 4:
    elif action == 4:
      searchShows()
    #case 5:
    elif action == 5:
      about()
    #case 6:
    elif action == 6:
      userSettings()
    #case 7:
    elif action == 7:
      sys.exit("[✔] Closed.")



if __name__ == "__main__":
  main()
