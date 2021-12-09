import json, sys, datetime, time, random, imdb

appInfo = {
  "Name": "Show List",
  "Creator": "Mark E",
  "Version": "1.3.1",
  "Description": "A program that allows you to keep track of shows you're watching."
}

guestShowsToWatch = []
guestShowsWatching = [{"Name": "None", "Episode": 1, "Status": "None"}]
guestCompletedShows = []
defaultName = "User"
accounts = []
assistantName = "Clover"
increment = 0
ia = imdb.IMDb()
selectedSearchedShow = None # Going to be used temporarily.

def checkLoggedIn():
  global accounts, name
  for a in accounts:
    if a["Logged In"]:
      name = a["Name"]
      return (True, a)
  return False

def completed():
  global accounts, guestCompletedShows
  if not checkLoggedIn():
    if not guestCompletedShows:
      input(f"[{assistantName}] 😅 < You haven't completed any shows yet! Try completing some shows first.")
    else:
      heading("Menu > Completed Shows")
      for title in guestCompletedShows:
        print(f"-> {title}")
      print("[i] Total items: " + str(len(guestCompletedShows)))
      print("[i] The ability to remove shows from your completed list will come in a future update!")
      input("Press ENTER to exit. | ")
  else:
    if not checkLoggedIn()[1]["CompletedShows"]:
      input(f"[{assistantName}] 😅 < You haven't completed any shows yet! Try completing some shows first.")
    else:
      heading("Menu > Completed Shows")
      for title in checkLoggedIn()[1]["CompletedShows"]:
        print(f"-> {title}")
      print("[i] Total items: " + str(len(checkLoggedIn()[1]["CompletedShows"])))
      print("[i] The ability to remove shows from your completed list will come in a future update!")
      input("Press ENTER to exit. | ")

def loopThroughShows():
  global accounts, increment, guestShowsWatching

  increment = 0

  if not checkLoggedIn():
    print("----------------------------------------------")
    for i in range(len(guestShowsWatching)):
      print(f"[{i}] | Show: {guestShowsWatching[i]['Name']} | EP: {guestShowsWatching[i]['Episode']} | Status: {guestShowsWatching[i]['Status']}")
    print("----------------------------------------------")
  else:
    print("----------------------------------------------")
    for i in range(len(checkLoggedIn()[1]["ShowsWatching"])):
      print(f"[{i}] | Show: {checkLoggedIn()[1]['ShowsWatching'][i]['Name']} | EP: {checkLoggedIn()[1]['ShowsWatching'][i]['Episode']} | Status: {checkLoggedIn()[1]['ShowsWatching'][i]['Status']}")
    print("----------------------------------------------")

def checkShow(show, location="both"):
  global accounts

  if not checkLoggedIn():
    if location == "both":
      for i in range(len(guestShowsToWatch)):
        if guestShowsToWatch[i]["Name"] == show:
          input(f"[{assistantName}] 😅 < Haha, you're already planning on watching this show!")
          return True
    
      for i in range(len(guestShowsWatching)):
        if guestShowsWatching[i]["Name"] == show:
          input(f"[{assistantName}] 😅 < Haha, you're already watching watching that show! Try again!")
          return True
  elif location == "watchingnow":
    for i in range(len(guestShowsWatching)):
      if guestShowsWatching[i]["Name"] == show:
        input(f"[{assistantName}] 😅 < Haha, you're already watching that show!")
        return True
  elif location == "watchinglater":
    for i in range(len(guestShowsToWatch)):
      if guestShowsToWatch[i]["Name"] == show:
        input(f"[{assistantName}] 😅 < Haha, you're already planning on watching that show!")
        return True
  else:
    if location == "both":
      for i in range(len(checkLoggedIn()[1]['ShowsToWatch'])):
        if checkLoggedIn()[1]['ShowsToWatch'][i]["Name"] == show:
          input(f"[{assistantName}] 😅 < Haha, you're already planning on watching this show!")
          return True
      
      for i in range(len(checkLoggedIn()[1]['ShowsWatching'])):
        if checkLoggedIn()[1]['ShowsWatching'][i]["Name"] == show:
          input(f"[{assistantName}] 😅 < Haha, you're already watching watching that show! Try again!")
          return True
    elif location == "watchingnow":
      for i in range(len(checkLoggedIn()[1]['ShowsWatching'])):
        if checkLoggedIn()[1]['ShowsWatching'][i]["Name"] == show:
          input(f"[{assistantName}] 😅 < Haha, you're already watching that show!")
          return True
    elif location == "watchinglater":
      for i in range(len(checkLoggedIn()[1]['ShowsToWatch'])):
        if checkLoggedIn()[1]['ShowsToWatch'][i]["Name"] == show:
          input(f"[{assistantName}] 😅 < Haha, you're already planning on watching that show!")
          return True
  return False

def addNewShow(show, episode: int, location):
  global accounts, selectedSearchedShow


  if not checkLoggedIn():
    if location == "watchingNow":
      if guestShowsWatching[0]["Name"] == "None":
        guestShowsWatching[0]["Name"] = show
        guestShowsWatching[0]["Episode"] = episode
        guestShowsWatching[0]["Status"] = "Watching"
      else:
        guestShowsWatching.append({"Name": show, "Episode": episode, "Status": "Watching"})
    elif location == "watchingLater":
      guestShowsToWatch.append({"Name": show, "Episode": episode})
    elif location == "both":
      if guestShowsWatching[0]["Name"] == "None":
        guestShowsWatching[0]["Name"] = show
        guestShowsWatching[0]["Episode"] = episode
        guestShowsWatching[0]["Status"] = "Watching"
      else:
        guestShowsWatching.append({"Name": show, "Episode": episode, "Status": "Watching"})
      guestShowsToWatch.append({"Name": show, "Episode": episode})
  else:
    if location == "watchingNow":
      if checkLoggedIn()[1]['ShowsWatching'][0]["Name"] == "None":
        checkLoggedIn()[1]['ShowsWatching'][0]["Name"] = show
        checkLoggedIn()[1]['ShowsWatching'][0]["Episode"] = episode
        checkLoggedIn()[1]['ShowsWatching'][0]["Status"] = "Watching"
      else:
        checkLoggedIn()[1]['ShowsWatching'].append({"Name": show, "Episode": episode, "Status": "Watching"})
    elif location == "watchingLater":
      checkLoggedIn()[1]['ShowsToWatch'].append({"Name": show, "Episode": episode})
    elif location == "both":
      if checkLoggedIn()[1]['ShowsWatching'][0]["Name"] == "None":
        checkLoggedIn()[1]['ShowsWatching'][0]["Name"] = show
        checkLoggedIn()[1]['ShowsWatching'][0]["Episode"] = episode
        checkLoggedIn()[1]['ShowsWatching'][0]["Status"] = "Watching"
      else:
        checkLoggedIn()[1]['ShowsWatching'].append({"Name": show, "Episode": episode, "Status": "Watching"})
      checkLoggedIn()[1]['ShowsToWatch'].append({"Name": show, "Episode": episode})
    json.dump(accounts, open("data.py", "w"), indent=2)
  

def showData(show, item="all"):
  try:
    if item == "all":
      if not checkLoggedIn():
        return (
        f"-> SHOW: {show.data['title']}\n"
        f"-> RATING: {str(show.data['rating'])} / 10.0\n"
        f"-> GENRES: {show.data['genres']}\n"
        f"-> YEAR: {show.data['year']}\n"
        f"-> VOTES: {str(show.data['votes'])}\n"
        f"-> ABOUT: {show.data['plot'][0]}\n"
        f"[{('✔' if show.data['title'] in [title['Name'] for title in guestShowsWatching] else '❌')}] Watching Now | [{('✔' if show.data['title'] in [title['Name'] for title in guestShowsToWatch] else '❌')}] Planning to Watch | [{('✔' if show.data['title'] in guestCompletedShows else '❌')}] Completed\n" if guestShowsToWatch and guestCompletedShows and guestShowsWatching else 
        f"-> SHOW: {show.data['title']}\n"
        f"-> RATING: {str(show.data['rating'])} / 10.0\n"
        f"-> GENRES: {show.data['genres']}\n"
        f"-> YEAR: {show.data['year']}\n"
        f"-> VOTES: {str(show.data['votes'])}\n"
        f"-> ABOUT: {show.data['plot'][0]}\n"
        "[!] Failed to get certain data, come back when all lists are loaded."
        )
      else:
        return (
        f"-> SHOW: {show.data['title']}\n"
        f"-> RATING: {str(show.data['rating'])} / 10.0\n"
        f"-> GENRES: {show.data['genres']}\n"
        f"-> YEAR: {show.data['year']}\n"
        f"-> VOTES: {str(show.data['votes'])}\n"
        f"-> ABOUT: {show.data['plot'][0]}\n"
        f"[{('✔' if show.data['title'] in [title['Name'] for title in checkLoggedIn()[1]['ShowsWatching']] else '❌')}] Watching Now | [{('✔' if show.data['title'] in [title['Name'] for title in checkLoggedIn()[1]['ShowsToWatch']] else '❌')}] Planning to Watch | [{('✔' if show.data['title'] in checkLoggedIn()[1]['CompletedShows'] else '❌')}] Completed\n" if checkLoggedIn()[1]["ShowsToWatch"] and checkLoggedIn()[1]["CompletedShows"] and checkLoggedIn()[1]["ShowsWatching"] else 
        f"-> SHOW: {show.data['title']}\n"
        f"-> RATING: {str(show.data['rating'])} / 10.0\n"
        f"-> GENRES: {show.data['genres']}\n"
        f"-> YEAR: {show.data['year']}\n"
        f"-> VOTES: {str(show.data['votes'])}\n"
        f"-> ABOUT: {show.data['plot'][0]}\n"
        "[!] Failed to get certain data, come back when all lists are loaded."
        )
    elif item == "title":
      return show.data['title']
    elif item == "year":
      return show.data['year']
    elif item == "rating":
      return show.data['rating']
    elif item == "votes":
      return show.data['votes']
    elif item == "genres":
      return show.data['genres']
    elif item == "plot":
      return show.data['plot'][0]
    elif item == "episodes":
      return ia.get_movie_episodes(show.movieID)["data"]["number of episodes"]
  except:
    return "[X] Something went wrong. Please contact [MARK] if you think there is a bug."

def findShow(show):
  global accounts, name, assistantName, selectedSearchedShow
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
    heading("Menu > Search > Show Information")
    print(showData(showTitle))
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

def create_account():
  global accounts
  heading("Welcome > Account > Create Account")
  print("[i] Step 1/3")
  print("| Let's get started with creating your account.")
  name = str(input("[i] Enter a username/name you'd like to be called as (back to exit): "))
  if name == "back":
    return
  while True:
    confirm = str(input(f"[i] Are you sure you want to create an account with the name {name}? (y/n) "))
    if confirm.strip().lower() == "y":
      for a in accounts:
        if a["Name"] == name:
          input(f"[X] Sorry, that name is already taken. Please try again.")
          break
      else:
        break
    name = str(input("[i] Enter a username/name you'd like to be called as (back to exit): "))
    if name == "back":
      return
  print("[i] Step 2/3")
  print("| Now, let's create a password for your account.")
  password = str(input("[i] Enter a password (back to exit): "))
  if password == "back":
    return
  while True:
    confirm = str(input(f"[i] Are you sure you want to use the password {password}? (y/n) "))
    if confirm.strip().lower() == "y":
      break
    password = str(input("[i] Enter a password (back to exit): "))
    if password == "back":
      return
  print("[i] Step 3/3")
  print("| Now, let's confirm your information.")
  print(
  f"| Username: {name}\n"
  f"| Password: {password}"
  )
  confirm = str(input("[i] Are you sure you want to create your account with the information above? (y/n) "))
  while True:
    if confirm.strip().lower() == "y":
      break
    create_account()
    return
  accounts.append({"Name": name, "Password": password, "Logged In": False, "ShowsToWatch": [], "ShowsWatching": [{"Name": "None", "Episode": 1, "Status": "None"}], "CompletedShows": []})
  json.dump(accounts, open("data.py", "w"), indent=2)
  print(f"[i] Your account has been created, you will now be redirected in a few seconds. Thank You!")
  time.sleep(random.randint(1, 3))

def login(username, password):
  global accounts
  for a in accounts:
    if a["Name"] == username and a["Password"] == password:
      return True
  return False

def welcome():
  global name
  heading("Welcome")
  input(
  f"| Welcome to {appInfo['Name']}.\n"
  "| Here, you can keep track of shows you're watching, and basically find information about shows.\n"
  "| Let's get started."
  )
  while True:
    heading("Welcome > Account")
    print(
      "| In order to get the best experience, it is recommended to create an account. It is not required, but without an account, you will have less features.\n"
      "| If you already have an account, select 'Log in', then continue from there. If not, select 'Create'.\n"
      "| If you are not sure what to do, select 'Exit', then come back later.\n"
      "[1] Create\n"
      "[2] Log in\n"
      "[3] Continue as Guest\n"
      "[4] Exit\n"
      "[5] Why use an account?"
      )
    option = input("| Enter Option > ")
    try:
      option = int(option)
    except:
      input("[X] Please enter a valid input.")
    if option == 1:
      create_account()
    elif option == 2:
      heading("Welcome > Account > Log In")
      print("| Welcome back, let's log you in.")
      user = str(input("[i] Enter your username (case sensitive!): "))
      password = str(input("[i] Enter your password (case sensitive!): "))
      if login(user, password):
        for a in accounts:
          if a["Name"] == user:
            a["Logged In"] = True
            name = a["Name"]
            print("[✔] Awesome! You're now logged in.")
            json.dump(accounts, open("data.py", "w"), indent=2)
            break
        break
      else:
        input("[X] Failure when trying to log in. Check to make sure both your username & password is correct.")
    elif option == 3:
      confirm = str(input("[i] Are you sure you want to continue as a guest? Logging into an account is highly recommended. (y/n) "))
      if confirm.strip().lower() == "y":
        name = "Guest"
        print("[i] Continuing as Guest...")
        break
    elif option == 4:
      quit("| See you later, maybe.")
    elif option == 5:
      heading("Welcome > Account > Why use an account?")
      input(
      "| An account is required in order to keep track of shows you're watching.\n"
      "| It is not required, but without an account, you will have less features, such as saving.\n"
      "| If you already have an account, select 'Log in', then continue from there. If not, select 'Create'.\n"
      )
  

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
  global accounts
  sys.stdout.write("[🔄] Fetching list...")
  sys.stdout.flush()
  sys.stdout.write("\r")
  sys.stdout.flush()

  if not checkLoggedIn():
    if not guestShowsToWatch:
      input("[X] Your list is empty! Go search for some shows to watch, then come here.")
    else:
      heading("Menu > Shows to Watch")
      for title in range(len(guestShowsToWatch)):
        print(f"[{title}] {guestShowsToWatch[title]['Name']}")
      print("[i] Total items: " + str(len(guestShowsToWatch)))
      print("[i] The ability to remove shows from this list will come in a future update!")
      print("| View [# next to title] | Exit [e]")
      action = input(">>> ")
      if action.strip().lower() == "e":
        return
      try:
        action = int(action)
      except ValueError:
        input("[X] Please enter a valid input.")
      if action in range(0, len(guestShowsToWatch)):
        heading("Menu > Shows to Watch > View Show")
        movie_id = ia.search_movie(guestShowsToWatch[action]['Name'].strip())[0].movieID # Search the show, get the first result, and get the movie ID.
        selected_show = ia.get_movie(movie_id) # Fetch the movie using the movie ID.
        print(showData(selected_show))
        return input("Press ENTER to exit. | ")
      else:
        input("[X] Please enter a valid input.")
  else:
    if not checkLoggedIn()[1]['ShowsToWatch']:
      input("[X] Your list is empty! Go search for some shows to watch, then come here.")
    else:
      heading("Menu > Shows to Watch")
      for title in range(len(checkLoggedIn()[1]['ShowsToWatch'])):
        print(f"[{title}] {checkLoggedIn()[1]['ShowsToWatch'][title]['Name']}")
      print("[i] Total items: " + str(len(checkLoggedIn()[1]['ShowsToWatch'])))
      print("[i] The ability to remove shows from this list will come in a future update!")
      print("| View [# next to title] | Exit [e]")
      action = input(">>> ")
      if action.strip().lower() == "e":
        return
      try:
        action = int(action)
      except ValueError:
        input("[X] Please enter a valid input.")
      if action in range(0, len(checkLoggedIn()[1]['ShowsToWatch'])):
        heading("Menu > Shows to Watch > View Show")
        movie_id = ia.search_movie(checkLoggedIn()[1]['ShowsToWatch'][action]['Name'].strip())[0].movieID # Search the show, get the first result, and get the movie ID.
        selected_show = ia.get_movie(movie_id) # Fetch the movie using the movie ID.
        print(showData(selected_show))
        return input("Press ENTER to exit. | ")
      else:
        input("[X] Please enter a valid input.")
      

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
  global accounts

  if not checkLoggedIn():
    heading("Menu > Currently Watching")
    for i in range(len(guestShowsWatching)):
      print(f"[{i}] | Show: {guestShowsWatching[i]['Name']} | EP: {guestShowsWatching[i]['Episode']} | Status: {guestShowsWatching[i]['Status']}")
    print("[i] Total items: " + str(len(guestShowsWatching)))
    print("| Change [c] | Remove [r] | Move to Completed [m] | View [v] | Exit [e]")
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
        if edit in range(0, len(guestShowsWatching)):
          title = str(input(f"[{assistantName}] 🧐 < What is the name of the show you're watching? ('e' to exit) "))
          if title.strip().lower() == "e":
            return
          if checkShow(title, "watchingNow"):
            return
          while True:
            update = str(input(f"[{assistantName}] 🙂 < You're currently watching '{title}'? (y/n) "))
            if update.strip().lower() == "y":
              break
            title = str(input(f"[{assistantName}] 🧐 < What is the name of the show you're watching? ('e' to exit) "))
            if title.strip().lower() == "e":
              return
          guestShowsWatching[edit]["Name"] = title
        else:
          return input("[X] Invalid number range.")
        print("[✔] Process complete.")
      elif change.strip().lower() == "episode":
        loopThroughShows()
        edit = input(f"[{assistantName}] 🤔 < Which show do you want to edit? ")
        try:
          edit = int(edit)
        except ValueError:
          input("[X] Invalid input, please try again!")
        if edit in range(0, len(guestShowsWatching)):
          episode = input(f"[{assistantName}] 🙂 < Please enter the episode number ('e' to exit). ")
          if episode.strip().lower() == "e":
            return
          try:
            episode = int(episode)
          except ValueError:
            input("[X] Invalid input, please try again!")
          while True:
            confirm = str(input(f"[{assistantName}] 🤔 < You're currently on episode {episode} on '{guestShowsWatching[edit]['Name']}'? (y/n)"))
            if confirm.strip().lower() == "y":
              break
            episode = input(f"[{assistantName}] 🙂 < Please enter the episode number ('e' to exit). ")
            if episode.strip().lower() == "e":
              return
            try:
              episode = int(episode)
            except ValueError:
              input("[X] Invalid input, please try again!")
          guestShowsWatching[edit]["Episode"] = episode
          if guestShowsWatching[edit]["Episode"] == showData(ia.search_movie(guestShowsWatching[edit]["Name"])[0], "episodes"):
            guestShowsWatching[edit]["Status"] = "Complete"
            return input(f"[✔] You've completed '{guestShowsWatching[edit]['Name']}'! Its status is now set to 'complete'.")
        else:
          return input("[X] Invalid number range.")
        print("[✔] Process complete.")
    elif action == "r":
      heading("Menu > Currently Watching > Remove Show")
      loopThroughShows()
      remove = input(f"[{assistantName}] 🤔 < Which show do you want to remove? ")
      try:
        remove = int(remove)
      except ValueError:
        input("[X] Invalid input, please try again!")
      confirm = str(input(f"[{assistantName}] 🤔 < Are you sure you want to remove '{guestShowsWatching[remove]['Name']}'? (y/n) "))
      if confirm.strip().lower() == "y":
        guestShowsWatching.pop(remove)
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
        if guestShowsWatching[move]['Status'] == "Watching":
          confirm = str(input(f"[{assistantName}] 🤔 < You aren't completed with '{guestShowsWatching[move]['Name']}' yet, do you still want to move it to your list of completed shows? (y/n) "))
          if confirm.strip().lower() == "y":
            guestCompletedShows.append(guestShowsWatching[move]['Name'])
            guestShowsWatching.pop(move)
            print("[✔] Nice, you finished a show!")
        elif guestShowsWatching[move]["Status"] == "Complete":
          confirm = str(input(f"[{assistantName}] 🧐 < You've completed '{guestShowsWatching[move]['Name']}'! Do you want to move this show to your list of completed shows? (y/n) "))
          if confirm.strip().lower() == "y":
            guestCompletedShows.append(guestShowsWatching[move]['Name'])
            guestShowsWatching.pop(move)
            print("[✔] Nice, you finished a show!")
    elif action == "v":
      heading("Menu > Currently Watching > View Show")
      loopThroughShows()
      view = input(f"[{assistantName}] 🤔 < Which show do you want to view? ")
      try:
        view = int(view)
      except ValueError:
        input("[X] Invalid input, please try again!")
      if view in range(0, len(guestShowsWatching)):
        movie_id = ia.search_movie(guestShowsWatching[view]['Name'].strip())[0].movieID # Search the show, get the first result, and get the movie ID.
        selected_show = ia.get_movie(movie_id) # Fetch the movie using the movie ID.
        print(showData(selected_show))
        input("Press ENTER to exit. |")
      else:
        return input("[X] Invalid number range.")
    else:
      return
  else:
    heading("Menu > Currently Watching")
    for i in range(len(checkLoggedIn()[1]['ShowsWatching'])):
      print(f"[{i}] | Show: {checkLoggedIn()[1]['ShowsWatching'][i]['Name']} | EP: {checkLoggedIn()[1]['ShowsWatching'][i]['Episode']} | Status: {checkLoggedIn()[1]['ShowsWatching'][i]['Status']}")
    print("[i] Total items: " + str(len(checkLoggedIn()[1]['ShowsWatching'])))
    print("| Change [c] | Remove [r] | Move to Completed [m] | View [v] | Exit [e]")
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
        if edit in range(0, len(checkLoggedIn()[1]['ShowsWatching'])):
          title = str(input(f"[{assistantName}] 🧐 < What is the name of the show you're watching? ('e' to exit) "))
          if title.strip().lower() == "e":
            return
          if checkShow(title, "watchingNow"):
            return
          while True:
            update = str(input(f"[{assistantName}] 🙂 < You're currently watching '{title}'? (y/n) "))
            if update.strip().lower() == "y":
              break
            title = str(input(f"[{assistantName}] 🧐 < What is the name of the show you're watching? ('e' to exit) "))
            if title.strip().lower() == "e":
              return
          checkLoggedIn()[1]['ShowsWatching'][edit]["Name"] = title
        else:
          return input("[X] Invalid number range.")
        print("[✔] Process complete.")
      elif change.strip().lower() == "episode":
        loopThroughShows()
        edit = input(f"[{assistantName}] 🤔 < Which show do you want to edit? ")
        try:
          edit = int(edit)
        except ValueError:
          input("[X] Invalid input, please try again!")
        if edit in range(0, len(checkLoggedIn()[1]['ShowsWatching'])):
          episode = input(f"[{assistantName}] 🙂 < Please enter the episode number ('e' to exit). ")
          if episode.strip().lower() == "e":
            return
          try:
            episode = int(episode)
          except ValueError:
            input("[X] Invalid input, please try again!")
          while True:
            confirm = str(input(f"[{assistantName}] 🤔 < You're currently on episode {episode} on '{checkLoggedIn()[1]['ShowsWatching'][edit]['Name']}'? (y/n)"))
            if confirm.strip().lower() == "y":
              break
            episode = input(f"[{assistantName}] 🙂 < Please enter the episode number ('e' to exit). ")
            if episode.strip().lower() == "e":
              return
            try:
              episode = int(episode)
            except ValueError:
              input("[X] Invalid input, please try again!")
          checkLoggedIn()[1]['ShowsWatching'][edit]["Episode"] = episode
          if checkLoggedIn()[1]['ShowsWatching'][edit]["Episode"] == showData(ia.search_movie(checkLoggedIn()[1]['ShowsWatching'][edit]["Name"])[0], "episodes"):
            checkLoggedIn()[1]['ShowsWatching'][edit]["Status"] = "Complete"
            return input(f"[✔] You've completed '{checkLoggedIn()[1]['ShowsWatching'][edit]['Name']}'! Its status is now set to 'complete'.")
        else:
          return input("[X] Invalid number range.")
        print("[✔] Process complete.")
    elif action == "r":
      heading("Menu > Currently Watching > Remove Show")
      loopThroughShows()
      remove = input(f"[{assistantName}] 🤔 < Which show do you want to remove? ")
      try:
        remove = int(remove)
      except ValueError:
        input("[X] Invalid input, please try again!")
      confirm = str(input(f"[{assistantName}] 🤔 < Are you sure you want to remove '{checkLoggedIn()[1]['ShowsWatching'][remove]['Name']}'? (y/n) "))
      if confirm.strip().lower() == "y":
        checkLoggedIn()[1]['ShowsWatching'].pop(remove)
        print("[✔] Show removed.")
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
        if checkLoggedIn()[1]['ShowsWatching'][move]['Status'] == "Watching":
          confirm = str(input(f"[{assistantName}] 🤔 < You aren't completed with '{checkLoggedIn()[1]['ShowsWatching'][move]['Name']}' yet, do you still want to move it to your list of completed shows? (y/n) "))
          if confirm.strip().lower() == "y":
            checkLoggedIn()[1]['CompletedShows'].append(checkLoggedIn()[1]['ShowsWatching'][move]['Name'])
            checkLoggedIn()[1]['ShowsWatching'].pop(move)
            print("[✔] Nice, you finished a show!")
        elif checkLoggedIn()[1]['ShowsWatching'][move]["Status"] == "Complete":
          confirm = str(input(f"[{assistantName}] 🧐 < You've completed '{checkLoggedIn()[1]['ShowsWatching'][move]['Name']}'! Do you want to move this show to your list of completed shows? (y/n) "))
          if confirm.strip().lower() == "y":
            checkLoggedIn()[1]['CompletedShows'].append(checkLoggedIn()[1]['ShowsWatching'][move]['Name'])
            checkLoggedIn()[1]['ShowsWatching'].pop(move)
            print("[✔] Nice, you finished a show!")
    elif action == "v":
      heading("Menu > Currently Watching > View Show")
      loopThroughShows()
      view = input(f"[{assistantName}] 🤔 < Which show do you want to view? ")
      try:
        view = int(view)
      except ValueError:
        input("[X] Invalid input, please try again!")
      if view in range(0, len(checkLoggedIn()[1]['ShowsWatching'])):
        movie_id = ia.search_movie(checkLoggedIn()[1]['ShowsWatching'][view]['Name'].strip())[0].movieID # Search the show, get the first result, and get the movie ID.
        selected_show = ia.get_movie(movie_id) # Fetch the movie using the movie ID.
        print(showData(selected_show))
        input("Press ENTER to exit. | ")
      else:
        return input("[X] Invalid number range.")
    else:
      return
    json.dump(accounts, open("data.py", "w"), indent=2)
    

def userSettings():
  global name, accounts
  heading("Menu > Settings")
  print(
    f"[{assistantName}] 🤔 What are you looking to change, {name}?\n"
    "[1] Change username/name.\n"
    "[2] Delete Account.\n"
    "[3] Sign Out.\n"
    "[4] Exit." if name != "Guest" else "[1] Exit Guest Mode.\n[2] Exit."
  )
  settings = input(">>> ")
  try:
    settings = int(settings)
  except ValueError:
    input("[X] Invalid input, please try again!")
  if settings == 1:
    if name == "Guest":
      # Ask if they want to leave guest mode
      print("[!] When in Guest Mode, your data will not be saved. Make sure to write any shows that you have on Guest Mode somewhere else so you do not lose them.")
      confirm = str(input(f"[{assistantName}] 🤔 < You're currently in guest mode, do you want to leave? (y/n) "))
      if confirm.strip().lower() == "y":
        print("| Leaving Guest Mode...")
        welcome()
    else:
      heading("Menu > Settings > Change Username")
      input(f"[{assistantName}] 🙂 < Oh? You want me to call you something else? Sure! What'll it be?")
      name = str(input("> Enter your new username/name: "))
      while True:
        confirm = input(f"[?] 🧐 {name}, so this is what you want to change your username/name to? (y/n)")
        if confirm.strip().lower() == "y":
          break
        name = str(input("> Enter your new username/name: "))
      checkLoggedIn()[1]["Name"] = name
      json.dump(accounts, open("data.py", "w"), indent=2)
      input(f"[{assistantName}] 😁 < Great, your username is now '{checkLoggedIn()[1]['Name']}'!")


  elif settings == 2:
    if name == "Guest":
      return
    else:
      heading("Menu > Settings > Delete Account")
      input(f"[{assistantName}] 😨 < Wha- You want to delete your account?! Why?!")
      input(f"[{assistantName}] 😔 < No no, I'm sorry. This must be something you're deciding on your own.")
      input(f"[{assistantName}] 😥 < You do know what this means right? All the shows you added will be GONE, for GOOD! I will also not remember you, {name}...")
      input(f"[{assistantName}] 😟 < Though, if you've come here, I'm sure you know. However, this is your choice, so I will not interfere with anything.")
      input(f"[{assistantName}] 😕 < So... what'll it be, {name}?")
      erase = input(
        "[!] By deleting your account, your name, list of shows, what your currently watching, and completed shows will be wiped. Are you sure you want to continue?\n"
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
          accounts.remove(checkLoggedIn()[1])
          print("[✔] Data erased successfully.")
          advance = str(input("[.] In order to continue using this program, you'll need to create a new account, or use Guest Mode. If you want to later, type 'exit', if you want to now, type 'new'. (new/exit) "))
          if advance.strip().lower() == "new":
            welcome()
          else:
            sys.exit("[✔] Closed.")
  elif settings == 3:
    if name != "Guest":
      heading("Menu > Settings > Sign Out")
      confirm = str(input(f"[{assistantName}] 😕 < Are you sure you want to sign out? (y/n)"))
      if confirm.strip().lower() == "y":
        for a in accounts:
          if a["Logged In"]:
            a["Logged In"] = False
            break
        print("[✔] Successfully signed out.")
        name = "Guest"
        json.dump(accounts, open("data.py", "w"), indent=2)
        welcome()


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
      if checkShow(selectedSearchedShow, location.strip().lower()):
        return
      addNewShow(selectedSearchedShow, episode, saveLocation)
      selectedSearchedShow = None
      print("[✔] Process complete.")
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
  global name, selectedSearchedShow, accounts

  try:
    accounts = json.load(open("data.py", "r"))
  except:
    print("[.] Some data didn't load.")

  if not checkLoggedIn():
    welcome()
  check_time(name)
  while True:
    print(
      "------------------------------------------\n"
      f"[{assistantName}] 😄 < {cloverGreeting()}\n"
      "[1] View your list of upcoming shows.\n"
      "[2] View what you're currently watching.\n"
      "[3] View completed shows.\n"
      "[4] Search Show.\n"
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
      if name == "Guest":
        warning = str(input("[!] You're in Guest Mode, and by exiting your data will be lost. Be sure to write down your shows somewhere else before exiting. Otherwise, do you really want to exit? (y/n)"))
        if warning.strip().lower() == "y":
          sys.exit("[✔] Closed.")
      else:
        sys.exit("[✔] Closed.")



if __name__ == "__main__":
  main()
