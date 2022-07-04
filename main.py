import json, sys, datetime, colorama
from random import randint
from time import sleep, time
from showlist import ShowList
from tabulate import tabulate
from colorama import Fore
from auth import *
from github.GithubException import BadCredentialsException, RateLimitExceededException
from imdb._exceptions import IMDbDataAccessError

def timeex(func):
  def wrapper(*args, **kwargs):
    start = time()
    result = func(*args, **kwargs)
    end = time()
    print(f"Execution time: {round(end - start, 2)} seconds")
    return result
  return wrapper

guestShowsToWatch = []
guestShowsWatching = []
guestCompletedShows = []
guestSettings = {"MaxResults": 10, "PlotPreview": False}
accounts = []
increment = 0
selectedSearchedShow = None
showList = ShowList() # Initialize the Show List class
statuses = ["Watching", "Complete", "Paused", "Dropped", "Uncertain", "Waiting"]
name: str = ""
colorama.init(autoreset=True)

def heading(text):
  for i in range(len(text)):
    print("-", end="")
  print()
  print(text)
  for i in range(len(text)):
    print("-", end="")
  print()

def checkForUpdates():
  sys.stdout.write("[.] Checking for updates...")
  sleep(0.5)

  if isinstance(showList.up_to_date(), bool):
    print(f"\r[{Fore.GREEN}SUCCESS{Fore.WHITE}] You're using the latest version of Show List.")
  elif not showList.up_to_date()[0]:
    print(
      "\r========================================================\n"
      f"{Fore.LIGHTYELLOW_EX}/!\{Fore.WHITE} A {Fore.YELLOW}new version{Fore.WHITE} is available!\n"
      ">>> Current version: " + str(showList.__version__) + " | Latest version: " + str(showList.up_to_date()[1]) + "\n"
      f"\nYou can download the latest version from: https://www.github.com/MarkE16/ShowList\n{Fore.RED}Note: Save data will not transfer, so you'll need to go into program's files and make a copy of the"
      f" data.json file, then transfer it to the new version. More information about updating on the Github page.{Fore.WHITE}\n"
      "========================================================\n"
    )
  else:
    input(showList.up_to_date())

def searchSettings():
  heading("Menu > Settings > Search Settings")
  print(
    "[1] Edit Max Search Results.\n"
    "[2] Toggle Plot Preview.\n"
    "[3] Exit."
  )
  choice = input(">>> ")
  try:
    choice = int(choice)
  except ValueError:
    input(f"[{Fore.RED}!{Fore.WHITE}] Invalid input.\n")
  if choice == 1:
    heading("Menu > Settings > Search Settings > Edit Max Search Results")
    print("[i] Current Max Number Set: " + str(guestSettings["MaxResults"] if not checkLoggedIn() else checkLoggedIn()[1]['Settings']['MaxResults']))
    while True:
      newMax = input("[i] Enter the new Max Number (e to exit): ")
      if newMax == "e":
        return
      try:
        newMax = int(newMax)
      except ValueError:
        input(f"[{Fore.RED}!{Fore.WHITE}] Invalid input.\n")
        continue
      if newMax < 1:
        input(f"[{Fore.RED}!{Fore.WHITE}] Number cannot be 0 or less.")
        continue
      confirm = input(f"[?] If increasing the limit, it may take longer to fetch results. Otherwise, confirm the change to {Fore.LIGHTYELLOW_EX}{newMax}{Fore.WHITE}? (y/n): ")
      if confirm == "y":
        break
    if not checkLoggedIn():
      guestSettings["MaxResults"] = newMax
    else:
      checkLoggedIn()[1]['Settings']['MaxResults'] = newMax
    print(f"[{Fore.GREEN}√{Fore.WHITE}] Max Search Results set to {Fore.LIGHTYELLOW_EX}{newMax}{Fore.WHITE}.")
  elif choice == 2:
    heading("Menu > Settings > Search Settings > Toggle Plot Preview")
    print("[i] Current Plot Preview Setting: " + str(guestSettings["PlotPreview"] if not checkLoggedIn() else checkLoggedIn()[1]['Settings']['PlotPreview']))
    print(f"[i] Tip: Disabling Plot Preview may {Fore.LIGHTGREEN_EX}decrease{Fore.WHITE} the time it takes to fetch results by {Fore.LIGHTYELLOW_EX}a lot{Fore.WHITE}, depending on the max limit.")
    print(
      "[1] Enable Plot Preview.\n"
      "[2] Disable Plot Preview."
    )
    choice = input(">>> ")
    try:
      choice = int(choice)
    except ValueError:
      input(f"[{Fore.RED}!{Fore.WHITE}] Invalid input.\n")
    if choice == 1:
      if not checkLoggedIn():
        if guestSettings["PlotPreview"]:
          input(f"[{Fore.RED}!{Fore.WHITE}] Plot Preview is already enabled.")
        else:
          guestSettings["PlotPreview"] = True
          print(f"[{Fore.GREEN}√{Fore.WHITE}] Plot Preview has been enabled.")
      else:
        if checkLoggedIn()[1]["Settings"]["PlotPreview"]:
          input(f"[{Fore.RED}!{Fore.WHITE}] Plot Preview is already enabled.")
        else:
          checkLoggedIn()[1]["Settings"]["PlotPreview"] = True
          print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Plot Preview has been enabled.")
    elif choice == 2:
      if not checkLoggedIn():
        if not guestSettings["PlotPreview"]:
          input(f"[{Fore.RED}!{Fore.WHITE}] Plot Preview is already disabled.")
        else:
          guestSettings["PlotPreview"] = False
          print(f"[{Fore.GREEN}√{Fore.WHITE}] Plot Preview has been disabled.")
      else:
        if not checkLoggedIn()[1]["Settings"]["PlotPreview"]:
          input(f"[{Fore.RED}!{Fore.WHITE}] Plot Preview is already disabled.")
        else:
          checkLoggedIn()[1]["Settings"]["PlotPreview"] = False
          print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Plot Preview has been disabled.")


def checkLoggedIn():
  global accounts
  for a in accounts:
    if a["Logged In"]:
      return (True, a)
  return False


def loopThroughShows(showList):
  if showList:
    return tabulate(showList, headers="keys", tablefmt="fancy_grid", showindex="always", numalign="center")
  return 0 # Return 0 if list is empty.


def completed():
  global accounts, guestCompletedShows
  if not checkLoggedIn():
    if not guestCompletedShows:
      input("[!] You haven't completed any shows yet. Try completing some shows first.")
    else:
      heading("Menu > Completed Shows")
      for show in guestCompletedShows:
        print("-> " + show)
      #print(loopThroughShows(guestCompletedShows))
      print("[i] Total items: " + str(len(guestCompletedShows)))
      print("| Remove [r] | Exit [e]")
      action = input(">>> ")
      if action.strip().lower() == "r":
        for i, show in enumerate(guestCompletedShows):
          print(f"[{i}] -> {show}")
        remove = input("[?] Which show would you like to remove? (e to exit)")
        if remove.strip().lower() == "e":
          return
        try:
          remove = int(remove)
        except ValueError:
          input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again.")
        if remove in range(0, len(guestCompletedShows)):
          while True:
            confirm = input("[?] Are you sure you want to remove '" + guestCompletedShows[remove] + "'? [y/n] ")
            if confirm.strip().lower() == "y":
              break
            remove = input("[?] Which show would you like to remove? ")
            try:
              remove = int(remove)
            except ValueError:
              input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again.")
          showList.remove_show(remove, guestCompletedShows)
          print("[✔] Removed show.")
  else:
    if not checkLoggedIn()[1]["CompletedShows"]:
      input("[!] You haven't completed any shows yet. Try completing some shows first.")
    else:
      heading("Menu > Completed Shows")
      for show in checkLoggedIn()[1]["CompletedShows"]:
        print("-> " + show)
      #print(loopThroughShows(checkLoggedIn()[1]["CompletedShows"]))
      print("[i] Total items: " + str(len(checkLoggedIn()[1]["CompletedShows"])))
      print("| Remove [r] | Exit [e]")
      action = input(">>> ")
      if action.strip().lower() == "r":
        for i, show in enumerate(checkLoggedIn()[1]["CompletedShows"]):
          print(f"[{i}] -> {show}")
        remove = input("[?] Which show would you like to remove? (e to exit)")
        if remove.strip().lower() == "e":
          return
        try:
          remove = int(remove)
        except ValueError:
          input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again.")
        if remove in range(0, len(checkLoggedIn()[1]["CompletedShows"])):
          while True:
            confirm = input("[?] Are you sure you want to remove '" + checkLoggedIn()[1]["CompletedShows"][remove] + "'? [y/n] ")
            if confirm.strip().lower() == "y":
              break
            remove = input("[?] Which show would you like to remove? ")
            try:
              remove = int(remove)
            except ValueError:
              input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again.")
          showList.remove_show(remove, checkLoggedIn()[1]["CompletedShows"])
          json.dump(accounts, open("data.json", "w"), indent=2)
          print("[✔] Removed show.")

def checkShow(show, location):
  global accounts

  if not checkLoggedIn():
    if location == "both":
      for s in guestShowsToWatch:
        if s == show:
          input("[!] You're already planning on watching this show.")
          return True
    
      for i in range(len(guestShowsWatching)):
        if guestShowsWatching[i]["Name"] == show:
          input("[!] Ops, you're already watching that show.")
          return True
    elif location == "watchingnow":
      for i in range(len(guestShowsWatching)):
        if guestShowsWatching[i]["Name"] == show:
          input("[!] Ops, you're already watching that show.")
          return True
    elif location == "watchinglater":
      for s in guestShowsToWatch:
          if s == show:
            input("[!] You're already planning on watching this show.")
            return True
  else:
    if location == "both":
      for s in checkLoggedIn()[1]['ShowsToWatch']:
        if s == show:
          input("[!] You're already planning on watching this show.")
          return True
      
      for i in range(len(checkLoggedIn()[1]['ShowsWatching'])):
        if checkLoggedIn()[1]['ShowsWatching'][i]["Name"] == show:
          input("[!] Ops, you're already watching that show.")
          return True
    elif location == "watchingnow":
      for i in range(len(checkLoggedIn()[1]['ShowsWatching'])):
        if checkLoggedIn()[1]['ShowsWatching'][i]["Name"] == show:
          input("[!] Ops, you're already watching that show.")
          return True
    elif location == "watchinglater":
      for s in checkLoggedIn()[1]['ShowsToWatch']:
        if s == show:
          input("[!] You're already planning on watching this show.")
          return True
  return False

def addNewShow(show, episode: int, location):
  global accounts


  if not checkLoggedIn():
    if location == "watchingnow":
      showList.add_show({"Name": show, "Episode": episode, "Status": "Watching", "Favorite": "☆"}, guestShowsWatching)
    elif location == "watchinglater":
      showList.add_show(show, guestShowsToWatch)
    elif location == "both":
      showList.add_show({"Name": show, "Episode": episode, "Status": "Watching", "Favorite": "☆"}, guestShowsWatching)
      showList.add_show(show, guestShowsToWatch)
  else:
    if location == "watchingnow":
      showList.add_show({"Name": show, "Episode": episode, "Status": "Watching", "Favorite": "☆"}, checkLoggedIn()[1]['ShowsWatching'])
    elif location == "watchinglater":
      showList.add_show(show, checkLoggedIn()[1]['ShowsToWatch'])
    elif location == "both":
      showList.add_show({"Name": show, "Episode": episode, "Status": "Watching", "Favorite": "☆"}, checkLoggedIn()[1]['ShowsWatching'])
      showList.add_show(show, checkLoggedIn()[1]['ShowsToWatch'])
    json.dump(accounts, open("data.json", "w"), indent=2)
  

@timeex
def showData(show, item="all"):
  try:
    if isinstance(show, int):
      data = showList.ia.get_movie(show)
    else:
      data = show.data
    if item == "all":
      if not checkLoggedIn():
        if showList.get_show_info(show, 'kind') == "movie":
          runtime = int(data['runtimes'][0])
          hrs = runtime / 60
          mins = runtime - (int(hrs) * 60)
          return (
            f"-> TITLE: {data['title']} - {data['kind'].capitalize()}\n"
            f"-> RUNTIME: {int(hrs)}hr(s) {mins}min(s)\n"
            f"-> RATING: {str(data['rating'])} / 10.0\n"
            f"-> GENRES: {data['genres']}\n"
            f"-> YEAR: {data['year']}\n"
            f"-> VOTES: {str(data['votes'])}\n"
            f"-> ABOUT: {data['plot'][0]}\n"
            f"-> IMDB LINK: {showList.get_show_info(show, 'url')}\n"
            f"[{Fore.RED}!{Fore.WHITE}] Movies aren't currently supported to added to 'Titles You're Watching'. They can be, but still ask for episode numbers, which don't exist for movies.\n"
          )
        else:
          return (
            f"-> TITLE: {data['title']} - {data['kind'].capitalize()}\n"
            f"-> EPISODES: {showList.get_show_info(show, 'episodes')} / SEASONS: {data['seasons']}\n"# + ("ON EPISODE: " + str(guestShowsWatching[guestShowsWatching.index(show)]["Episode"]) if show in guestShowsWatching else "") + "\n"
            f"-> RATING: {str(data['rating'])} / 10.0\n"
            f"-> GENRES: {data['genres']}\n"
            f"-> YEAR: {data['year']}\n"
            f"-> VOTES: {str(data['votes'])}\n"
            f"-> ABOUT: {data['plot'][0]}\n"
            f"-> IMDB LINK: {showList.get_show_info(show, 'url')}\n"
            f"[{(f'{Fore.LIGHTGREEN_EX}√{Fore.WHITE}' if show.data['title'] in [title['Name'] for title in guestShowsWatching] else f'{Fore.LIGHTRED_EX}X{Fore.WHITE}')}] Watching Now | [{(f'{Fore.LIGHTGREEN_EX}√{Fore.WHITE}' if show.data['title'] in guestShowsToWatch else f'{Fore.LIGHTRED_EX}X{Fore.WHITE}')}] Planning to Watch | [{(f'{Fore.LIGHTGREEN_EX}√{Fore.WHITE}' if show.data['title'] in guestCompletedShows else f'{Fore.LIGHTRED_EX}X{Fore.WHITE}')}] Completed\n"
          )
      else:
        if data['kind'] == "movie":
          runtime = int(data['runtimes'][0])
          hrs = runtime / 60
          mins = runtime - (int(hrs) * 60)
          return (
            f"-> TITLE: {data['title']} - {data['kind'].capitalize()}\n"
            f"-> RUNTIME: {int(hrs)}hr(s) {mins}min(s)\n"
            f"-> RATING: {str(data['rating'])} / 10.0\n"
            f"-> GENRES: {data['genres']}\n"
            f"-> YEAR: {data['year']}\n"
            f"-> VOTES: {str(data['votes'])}\n"
            f"-> ABOUT: {data['plot'][0]}\n"
            f"-> IMDB LINK: {showList.get_show_info(show, 'url')}\n"
            f"[{Fore.RED}!{Fore.WHITE}] Movies aren't currently supported to added to 'Titles You're Watching'. They can be, but still ask for episode numbers, which don't exist for movies.\n"
            #f"[{(f'{Fore.LIGHTGREEN_EX}√{Fore.WHITE}' if show.data['title'] in [title['Name'] for title in checkLoggedIn()[1]['ShowsWatching']] else f'{Fore.LIGHTRED_EX}X{Fore.WHITE}')}] Watching Now | [{(f'{Fore.LIGHTGREEN_EX}√{Fore.WHITE}' if show.data['title'] in checkLoggedIn()[1]['ShowsToWatch'] else f'{Fore.LIGHTRED_EX}X{Fore.WHITE}')}] Planning to Watch | [{(f'{Fore.LIGHTGREEN_EX}√{Fore.WHITE}' if show.data['title'] in checkLoggedIn()[1]['ShowsCompleted'] else f'{Fore.LIGHTRED_EX}X{Fore.WHITE}')}] Completed\n"
          )
        else:
          index:int
          titles = [title['Name'] for title in checkLoggedIn()[1]['ShowsWatching']]
          if data['title'] in titles:
            index = titles.index(data['title'])
          return (
            f"-> TITLE: {data['title']} - {data['kind'].capitalize()}\n"
            f"-> EPISODES: {showList.get_show_info(show, 'episodes')} / SEASONS: {data['seasons']}" + (" / ON EPISODE: " + str(checkLoggedIn()[1]['ShowsWatching'][index]["Episode"]) if data['title'] in [title['Name'] for title in checkLoggedIn()[1]['ShowsWatching']] else "") + "\n"
            f"-> RATING: {str(data['rating'])} / 10.0\n"
            f"-> GENRES: {data['genres']}\n"
            f"-> YEAR: {data['year']}\n"
            f"-> VOTES: {str(data['votes'])}\n"
            f"-> ABOUT: {data['plot'][0]}\n"
            f"-> IMDB LINK: {showList.get_show_info(show, 'url')}\n"
            f"[{(f'{Fore.LIGHTGREEN_EX}√{Fore.WHITE}' if data['title'] in [title['Name'] for title in checkLoggedIn()[1]['ShowsWatching']] else f'{Fore.LIGHTRED_EX}X{Fore.WHITE}')}] Watching Now | [{(f'{Fore.LIGHTGREEN_EX}√{Fore.WHITE}' if data['title'] in checkLoggedIn()[1]['ShowsToWatch'] else f'{Fore.LIGHTRED_EX}X{Fore.WHITE}')}] Planning to Watch | [{(f'{Fore.LIGHTGREEN_EX}√{Fore.WHITE}' if data['title'] in checkLoggedIn()[1]['CompletedShows'] else f'{Fore.LIGHTRED_EX}X{Fore.WHITE}')}] Completed\n"
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
      return showList.get_show_info(show, 'episodes')
  except KeyError as err:
    return "[X] Something went wrong when fetching data. Error: Missing key - " + str(err)
  except IMDbDataAccessError as err:
    return "[X] Something went wrong when fetching data. Error: IMDbDataAccessError - " + str(err)

def findShow(show):
  global accounts, name, selectedSearchedShow
  if not checkLoggedIn():
    loggedInLimit = guestSettings["MaxResults"]
  else:
    loggedInLimit = checkLoggedIn()[1]["Settings"]["MaxResults"]
  shows = showList.search_show(show, loggedInLimit)
  if shows:
    for i, title in enumerate(shows):
      if not checkLoggedIn():
        if guestSettings["PlotPreview"]:
          try:
            plot = showList.ia.get_movie(title.movieID).data['plot'][0]
            print(f"[{i}] | {title['long imdb canonical title']} | {(plot[:60] + '...' if len(plot) > 60 else plot)}")
          except KeyError:
            print(f"[{i}] | {title['long imdb canonical title']} | No plot preview available.")
        else:
          print(f"[{i}] | {title['long imdb canonical title']}")
      else:
        if checkLoggedIn()[1]["Settings"]["PlotPreview"]:
          try:
            plot = showList.ia.get_movie(title.movieID).data['plot'][0]
            print(f"[{i}] | {title['long imdb canonical title']} | {(plot[:60] + '...' if len(plot) > 60 else plot)}")
          except KeyError:
            print(f"[{i}] | {title['long imdb canonical title']} | No plot preview available.")
        else:
          print(f"[{i}] | {title['long imdb canonical title']}")
    print(f"[i] ITEMS: {loggedInLimit} (MAX)" if len(shows) == loggedInLimit else "[i] ITEMS: " + str(len(shows)))
    chosenShow = input("[?] Which title would you like to view? (e to exit)")
    if chosenShow.strip().lower() == "e":
      return
    else:
      while True:
        try:
          chosenShow = int(chosenShow)
          break
        except:
          input(f"[{Fore.RED}X{Fore.WHITE}] Please enter a valid number.")
          chosenShow = input("[?] Which title would you like to view? (e to exit)")
    showTitle = int(shows[chosenShow].movieID)
    heading("Menu > Search > Show Information")
    print(showData(showTitle))
    selectedSearchedShow = str(showList.get_show_info(showTitle, 'title'))
    return True
  return False

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
          input(f"[{Fore.RED}X{Fore.WHITE}] Sorry, that name is already taken. Please try again.")
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
  accounts.append({"Name": name, "Password": password, "Logged In": False, "ShowsToWatch": [], "ShowsWatching": [], "CompletedShows": []})
  json.dump(accounts, open("data.json", "w"), indent=2)
  print("[i] Your account has been created, you will now be redirected in a few seconds. Thank You!")
  sleep(randint(1, 3))

def login(username, password):
  global accounts
  for a in accounts:
    if a["Name"] == username and a["Password"] == password:
      return True
  return False

def welcome():
  global name
  while True:
    heading("Welcome > Account")
    print(
      f"| Welcome to {Fore.BLUE}{showList.__programname__}{Fore.WHITE}, the program to manage all the shows you like. Select an option to get started.\n"
      "[1] Create Account\n"
      "[2] Log In\n"
      "[3] Continue as Guest\n"
      "[4] Exit\n"
      "[5] Why use an account?\n"
      "\n"
      f"{Fore.YELLOW}* {showList.__programname__} | {showList.__copyright__} | {showList.__version__}"
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
            print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Awesome! You're now logged in.\n")
            json.dump(accounts, open("data.json", "w"), indent=2)
            break
        break
      else:
        input(f"[{Fore.RED}X{Fore.WHITE}]Failure when trying to log in. Check to make sure both your username & password is correct.")
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
  sys.stdout.write("\r")

  if not checkLoggedIn():
    if not guestShowsToWatch:
      input(f"[{Fore.RED}X{Fore.WHITE}] Your list is empty! Go search for some shows to watch, then come here.")
    else:
      heading("Menu > Shows to Watch")
      for i, show in enumerate(guestShowsToWatch):
        print(f"[{i}] {show}")
      #print(loopThroughShows(guestShowsToWatch))
      print("[i] Total items: " + str(len(guestShowsToWatch)))
      print("| View [#] | Remove [r] | Exit [e]")
      action = input(">>> ")
      if action.strip().lower() == "e":
        return
      elif action == "r":
        for i, show in enumerate(guestShowsToWatch):
          print(f"[{i}] {show}")
        remove = input("[i] Enter the number of the show you want to remove: ")
        try:
          remove = int(remove)
        except ValueError:
          input(f"[{Fore.RED}X{Fore.WHITE}] Please enter a valid input.")
        if remove in range(0, len(guestShowsToWatch)):
          while True:
            confirm = input(f"[i] Are you sure you want to remove '{guestShowsToWatch[remove]}'? (y/n) ")
            if confirm.strip().lower() == "y":
              break
            remove = input("[i] Enter the number of the show you want to remove: ")
            try:
              remove = int(remove)
            except ValueError:
              input(f"[{Fore.RED}X{Fore.WHITE}] Please enter a valid input.")
          showList.remove_show(remove, guestShowsToWatch)
          return print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Show removed.")
      try:
        action = int(action)
      except ValueError:
        input(f"[{Fore.RED}X{Fore.WHITE}] Please enter a valid input.")
      if action in range(0, len(guestShowsToWatch)):
        heading("Menu > Shows to Watch > View Show")
        movie_id = showList.ia.search_movie(guestShowsToWatch[action].strip())[0].movieID # Search the show, get the first result, and get the movie ID.
        selected_show = showList.ia.get_movie(movie_id) # Fetch the movie using the movie ID.
        print(showData(selected_show))
        return input("Press ENTER to exit. | ")
      else:
        input(f"[{Fore.RED}X{Fore.WHITE}] Please enter a valid input.")
  else:
    if not checkLoggedIn()[1]['ShowsToWatch']:
      input(f"[{Fore.RED}X{Fore.WHITE}] Your list is empty! Go search for some shows to watch, then come here.")
    else:
      heading("Menu > Shows to Watch")
      for i, show in enumerate(checkLoggedIn()[1]['ShowsToWatch']):
        print(f"[{i}] {show}")
      #print(loopThroughShows(checkLoggedIn()[1]['ShowsToWatch']))
      print("[i] Total items: " + str(len(checkLoggedIn()[1]['ShowsToWatch'])))
      print("| View [#] | Remove [r] | Exit [e]")
      action = input(">>> ")
      if action.strip().lower() == "e":
        return
      elif action == "r":
        for i, show in enumerate(checkLoggedIn()[1]['ShowsToWatch']):
          print(f"[{i}] {show}")
        remove = input("[i] Enter the number of the show you want to remove: ")
        try:
          remove = int(remove)
        except ValueError:
          input(f"[{Fore.RED}X{Fore.WHITE}] Please enter a valid input. 0 - {str(len(checkLoggedIn()[1]['ShowsToWatch']) - 1)}")
        if remove in range(0, len(checkLoggedIn()[1]['ShowsToWatch'])):
          while True:
            confirm = input(f"[i] Are you sure you want to remove '{checkLoggedIn()[1]['ShowsToWatch'][remove]}'? (y/n) ")
            if confirm.strip().lower() == "y":
              break
            remove = input("[i] Enter the number of the show you want to remove: ")
            try:
              remove = int(remove)
            except ValueError:
              input(f"[{Fore.RED}X{Fore.WHITE}] Please enter a valid input. 0 - {str(len(checkLoggedIn()[1]['ShowsToWatch']) - 1)}")
          showList.remove_show(remove, checkLoggedIn()[1]['ShowsToWatch'])
          json.dump(accounts, open("data.json", "w"), indent=2)
          return print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Show removed.")

      try:
        action = int(action)
      except ValueError:
        input(f"[{Fore.RED}X{Fore.WHITE}] Please enter a valid input.")
      if action in range(0, len(checkLoggedIn()[1]['ShowsToWatch'])):
        heading("Menu > Shows to Watch > View Show")
        selected_show = int(showList.ia.search_movie(checkLoggedIn()[1]['ShowsToWatch'][action].strip())[0].movieID) # Search the show, get the first result, and get the movie ID.
        print(showData(selected_show))
        return input("Press ENTER to exit. | ")
      else:
        input(f"[{Fore.RED}X{Fore.WHITE}] Please enter a valid input.")

def watching():
  global accounts

  if not checkLoggedIn():
    heading("Menu > Currently Watching")
    if loopThroughShows(guestShowsWatching) == 0:
      return input("[i] Nothing to display. Come back when you have something to watch. | ")
    print(loopThroughShows(guestShowsWatching))
    print("[i] Total items: " + str(len(guestShowsWatching)))
    print("| Change [c] | Remove [r] | Move to Completed [m] | View [v] | Favorite [f] | Exit [e]")
    action = str(input(">>> "))
    if action == "c":
      print(loopThroughShows(guestShowsWatching if not checkLoggedIn() else checkLoggedIn()[1]['ShowsWatching']))
      edit = input("[?] Which title do you want to edit? ") 
      try:
        edit = int(edit)
      except ValueError:
        input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
      if edit in range(0, len(guestShowsWatching)):
        change = str(input("[?] Change what about this title? (episode/status) "))
        if change.strip().lower() == "episode":
          episode = input("[?] Enter the episode number. ('e' to exit). ")
          if episode.strip().lower() == "e":
            return
          try:
            episode = int(episode)
          except ValueError:
            input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
          while True:
            confirm = str(input(f"[?] You're currently on episode {episode} on '{guestShowsWatching[edit]['Name']}'? (y/n)"))
            if confirm.strip().lower() == "y":
              break
            episode = input("[?] Enter the episode number. ('e' to exit). ")
            if episode.strip().lower() == "e":
              return
            try:
              episode = int(episode)
            except ValueError:
              input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
          guestShowsWatching[edit]["Episode"] = episode
          if guestShowsWatching[edit]["Episode"] == showData(showList.ia.search_movie(guestShowsWatching[edit]["Name"])[0], "episodes"):
            guestShowsWatching[edit]["Status"] = "Complete"
            return input(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] You've completed '{guestShowsWatching[edit]['Name']}'! Its status is now set to 'complete'.")
          print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Process complete.")
        elif change.strip().lower() == "status":
          print("[i] Status for '" + guestShowsWatching[edit]["Name"] + "': " + guestShowsWatching[edit]["Status"])
          for i, item in enumerate(statuses):
            print(f"[{i}] {item}")
          status = input("[.] Enter the status that fits best. ('e' to exit) ")
          if status.strip().lower() == "e":
            return
          try:
            status = int(status)
          except ValueError:
            input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
          if status in range(0, 6):
            guestShowsWatching[edit]["Status"] = statuses[status]
            print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Process complete.")
          else:
            return input(f"[{Fore.RED}X{Fore.WHITE}] Invalid number range. Valid range: 0-5.")
      else:
        return input(f"[{Fore.RED}X{Fore.WHITE}] Invalid number range. Valid range: 0 - " + str(len(guestShowsWatching) - 1) + ".")
    elif action == "r":
      heading("Menu > Currently Watching > Remove Show")
      print(loopThroughShows(guestShowsWatching if not checkLoggedIn() else checkLoggedIn()[1]['ShowsWatching']))
      remove = input("[?] Which title do you want to remove? ")
      try:
        remove = int(remove)
      except ValueError:
        input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
      if remove in range(0, len(guestShowsWatching)):
        confirm = str(input(f"[?] Are you sure you want to remove '{guestShowsWatching[remove]['Name']}'? (y/n) "))
        if confirm.strip().lower() == "y":
          showList.remove_show(remove, guestShowsWatching)
          input(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Removed title.")
      else:
        input(f"[{Fore.RED}X{Fore.WHITE}] Invalid number range. Valid range: 0 - " + str(len(guestShowsWatching) - 1) + ".")
    elif action == "m":
      heading("Menu > Currently Watching > Move Show")
      print(loopThroughShows(guestShowsWatching if not checkLoggedIn() else checkLoggedIn()[1]['ShowsWatching']))
      move = input("[?] Which title do you want to move? ")
      if move.strip().lower() == "e":
        return
      else:
        try:
          move = int(move)
        except ValueError:
          input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
        if move in range(0, len(guestShowsWatching)):
          if guestShowsWatching[move]['Status'] != "Complete":
            confirm = str(input(f"[?] You aren't completed with '{guestShowsWatching[move]['Name']}' yet, continue anyway? (y/n) "))
            if confirm.strip().lower() == "y":
              guestCompletedShows.append(guestShowsWatching[move]['Name'])
              guestShowsWatching.pop(move)
              print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Nice, you finished a title!")
            else:
              return
          confirm = str(input(f"[?] You've completed '{guestShowsWatching[move]['Name']}'! Do you want to move this show to your list of completed shows? (y/n) "))
          if confirm.strip().lower() == "y":
            guestCompletedShows.append(guestShowsWatching[move]['Name'])
            guestShowsWatching.pop(move)
            print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Nice, you finished a title!")
        else:
          input(f"[{Fore.RED}X{Fore.WHITE}] Invalid number range. Valid range: 0 - " + str(len(guestShowsWatching) - 1) + ".")
    elif action == "v":
      heading("Menu > Currently Watching > View Show")
      print(loopThroughShows(guestShowsWatching if not checkLoggedIn() else checkLoggedIn()[1]['ShowsWatching']))
      view = input("[?] Which title do you want to view? ")
      try:
        view = int(view)
      except ValueError:
        input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
      if view in range(0, len(guestShowsWatching)):
        movie_id = showList.ia.search_movie(guestShowsWatching[view]['Name'].strip())[0].movieID # Search the show, get the first result, and get the movie ID.
        selected_show = showList.ia.get_movie(movie_id) # Fetch the movie using the movie ID.
        print("[.] Hang on while we fetch the title...")
        print(showData(selected_show))
        input("Press ENTER to exit. |")
      else:
        return input(f"[{Fore.RED}X{Fore.WHITE}] Invalid number range. Valid range: 0 - " + str(len(guestShowsWatching) - 1) + ".")
    elif action == "f":
      heading("Menu > Currently Watching > Favorite")
      print(loopThroughShows(guestShowsWatching if not checkLoggedIn() else checkLoggedIn()[1]['ShowsWatching']))
      favorite = input("[?] Which title do you want to favorite? ")
      try:
        favorite = int(favorite)
      except ValueError:
        input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
      # if favorite in range(0, len(guestShowsWatching)):
      #   #if guestShowsWatching[favorite]['Favorite']
    else:
      return
  else:
    heading("Menu > Currently Watching")
    print(loopThroughShows(guestShowsWatching if not checkLoggedIn() else checkLoggedIn()[1]['ShowsWatching']))
    print("[i] Total items: " + str(len(checkLoggedIn()[1]['ShowsWatching'])))
    print("| Change [c] | Remove [r] | Move to Completed [m] | View [v] | Exit [e]")
    action = str(input(">>> "))
    if action == "c":
      print(loopThroughShows(guestShowsWatching if not checkLoggedIn() else checkLoggedIn()[1]['ShowsWatching']))
      edit = input("[?] Which title do you want to edit? ") 
      try:
        edit = int(edit)
      except ValueError:
        input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
      if edit in range(0, len(checkLoggedIn()[1]['ShowsWatching'])):
        change = str(input("[?] Change what about this title? (episode/status) "))
        if change.strip().lower() == "episode":
          episode = input("[?] Enter the episode number. ('e' to exit). ")
          if episode.strip().lower() == "e":
            return
          try:
            episode = int(episode)
          except ValueError:
            input("[X] Invalid input, please try again!")
          while True:
            confirm = str(input(f"[?] You're currently on episode {episode} on '{checkLoggedIn()[1]['ShowsWatching'][edit]['Name']}'? (y/n)"))
            if confirm.strip().lower() == "y":
              break
            episode = input("[?] Enter the episode number. ('e' to exit). ")
            if episode.strip().lower() == "e":
              return
            try:
              episode = int(episode)
            except ValueError:
              input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
          checkLoggedIn()[1]['ShowsWatching'][edit]["Episode"] = episode
          if checkLoggedIn()[1]['ShowsWatching'][edit]["Episode"] == showList.get_show_info(checkLoggedIn()[1]['ShowsWatching'][edit]["Name"], "episodes"):
            checkLoggedIn()[1]['ShowsWatching'][edit]["Status"] = "Complete"
            return input(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] You've completed '{Fore.LIGHTYELLOW_EX}{checkLoggedIn()[1]['ShowsWatching'][edit]['Name']}{Fore.WHITE}'! Its status is now set to 'complete'.")
          print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Process complete.")
        elif change.strip().lower() == "status":
          print("[i] Status for '" + checkLoggedIn()[1]['ShowsWatching'][edit]["Name"] + "': " + checkLoggedIn()[1]['ShowsWatching'][edit]["Status"])
          for i, item in enumerate(statuses):
            print(f"[{i}] {item}")
          status = input("[.] Enter the status that fits best. ('e' to exit) ")
          if status.strip().lower() == "e":
            return
          try:
            status = int(status)
          except ValueError:
            input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
          if status in range(0, 6):
            checkLoggedIn()[1]['ShowsWatching'][edit]["Status"] = statuses[status]
            print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Process complete.")
          else:
            return input(f"[{Fore.RED}X{Fore.WHITE}] Invalid number range. Valid range: 0-5.")
      else:
        return input("[X] Invalid number range. Valid range: 0 - " + str(len(checkLoggedIn()[1]['ShowsWatching']) - 1) + ".")
    elif action == "r":
      heading("Menu > Currently Watching > Remove Show")
      print(loopThroughShows(guestShowsWatching if not checkLoggedIn() else checkLoggedIn()[1]['ShowsWatching']))
      remove = input("[?] Which title do you want to remove? ")
      try:
        remove = int(remove)
      except ValueError:
        input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
      if remove in range(0, len(checkLoggedIn()[1]['ShowsWatching'])):
        confirm = str(input(f"[?] Are you sure you want to remove '{checkLoggedIn()[1]['ShowsWatching'][remove]['Name']}'? (y/n) "))
        if confirm.strip().lower() == "y":
          showList.remove_show(remove, checkLoggedIn()[1]['ShowsWatching'])
          print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Show removed.")
      else:
        return input(f"[{Fore.RED}X{Fore.WHITE}] Invalid number range. Valid range: 0 - " + str(len(checkLoggedIn()[1]['ShowsWatching']) - 1) + ".")
    elif action == "m":
      heading("Menu > Currently Watching > Move Show")
      print(loopThroughShows(guestShowsWatching if not checkLoggedIn() else checkLoggedIn()[1]['ShowsWatching']))
      move = input("[?] Which title do you want to move? ")
      if move.strip().lower() == "e":
        return
      else:
        try:
          move = int(move)
        except ValueError:
          input(f"[{Fore.RED}X{Fore.WHITE}] Invalid input, please try again!")
        if move in range(0, len(checkLoggedIn()[1]['ShowsWatching'])):
          if checkLoggedIn()[1]['ShowsWatching'][move]['Status'] != "Complete":
            confirm = str(input(f"[?] You aren't completed with '{checkLoggedIn()[1]['ShowsWatching'][move]['Name']}' yet, continue anyway? (y/n) "))
            if confirm.strip().lower() == "y":
              checkLoggedIn()[1]['CompletedShows'].append(checkLoggedIn()[1]['ShowsWatching'][move]['Name'])
              checkLoggedIn()[1]['ShowsWatching'].pop(move)
              return print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Nice, you finished a show!")
            else:
              return
          confirm = str(input(f"[?] You've completed '{checkLoggedIn()[1]['ShowsWatching'][move]['Name']}'! Do you want to move this show to your list of completed shows? (y/n) "))
          if confirm.strip().lower() == "y":
            checkLoggedIn()[1]['CompletedShows'].append(checkLoggedIn()[1]['ShowsWatching'][move]['Name'])
            checkLoggedIn()[1]['ShowsWatching'].pop(move)
            print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Nice, you finished a show!")
        else:
          return input(f"[{Fore.RED}X{Fore.WHITE}] Invalid number range. Valid range: 0 - " + str(len(checkLoggedIn()[1]['ShowsWatching']) - 1) + ".")
    elif action == "v":
      heading("Menu > Currently Watching > View Show")
      print(loopThroughShows(guestShowsWatching if not checkLoggedIn() else checkLoggedIn()[1]['ShowsWatching']))
      view = input("[?] Which title do you want to view? ")
      try:
        view = int(view)
      except ValueError:
        input("[X] Invalid input, please try again!")
      if view in range(0, len(checkLoggedIn()[1]['ShowsWatching'])):
        movie_id = showList.ia.search_movie(checkLoggedIn()[1]['ShowsWatching'][view]['Name'].strip())[0].movieID # Search the show, get the first result, and get the movie ID.
        movie_id = int(movie_id)
        print("[.] Hang on while we fetch the title...")
        print(showData(movie_id))
        input("Press ENTER to exit. | ")
      else:
        return input(f"[{Fore.RED}X{Fore.WHITE}] Invalid number range. Valid range: 0 - " + str(len(checkLoggedIn()[1]['ShowsWatching']) - 1) + ".")
    else:
      return
    json.dump(accounts, open("data.json", "w"), indent=2)

def about():
  heading("Menu > App Information")
  print(
    f"-> Program Name: {showList.__programname__}\n"
    f"-> Program Creator: {showList.__author__}\n"
    f"-> Program Version: {showList.__version__}\n"
    f"-> Program Description: {showList.__description__}\n"
  )
  print("| Check for Updates [u] | Exit [e]")
  action = str(input(">>> "))
  if action.strip().lower() == "u":
    try:
      checkForUpdates()
    except BadCredentialsException as err:
      print(f"\r[{Fore.RED}!{Fore.WHITE}] Failed to fetch update info. Reason -> {err}. Please try again later when credentials are valid.")
    except RateLimitExceededException as err:
      print(f"\r[{Fore.RED}!{Fore.WHITE}] Failed to fetch update info. Reason -> {err}. Please try again later on {showList.get_rate_limit_reset()}")
    about()
  elif action.strip().lower() == "e":
    return

def userSettings():
  global name, accounts
  heading("Menu > Settings")
  print(
    f"What do you want to look at, {Fore.LIGHTCYAN_EX}{name}{Fore.WHITE}?\n"
    "[1] Change username/name.\n"
    f"[2] {Fore.LIGHTRED_EX}Delete Account.{Fore.WHITE}\n"
    f"[3] {Fore.YELLOW}Sign Out.{Fore.WHITE}\n"
    f"[4] {Fore.LIGHTBLUE_EX}About The Program.{Fore.WHITE}\n"
    f"[5] {Fore.LIGHTGREEN_EX}Search Settings.{Fore.WHITE}\n"
    "[6] Exit." if name != "Guest" else f"[1] {Fore.LIGHTRED_EX}Exit Guest Mode.{Fore.WHITE}\n[2] {Fore.LIGHTBLUE_EX}About The Program{Fore.WHITE}\n[3] {Fore.LIGHTGREEN_EX}Search Settings{Fore.WHITE}.\n[4] Exit."
  )
  settings = input(">>> ")
  try:
    settings = int(settings)
  except ValueError:
    input("[X] Invalid input, please try again!")
  if settings == 1:
    if name == "Guest":
      # Ask if they want to leave guest mode
      print(f"[!] When in Guest Mode, your data will {Fore.LIGHTRED_EX}not{Fore.WHITE} be saved. Make sure to write any shows that you have on Guest Mode somewhere else so you do not lose them.")
      confirm = str(input("[?] You're currently in guest mode, do you want to leave? (y/n) "))
      if confirm.strip().lower() == "y":
        print("| Leaving Guest Mode...")
        welcome()
    else:
      heading("Menu > Settings > Change Username")
      name = str(input("> Enter your new username/name: "))
      while True:
        confirm = input(f"[?] {Fore.LIGHTYELLOW_EX}{name}{Fore.WHITE}, so this is what you want to change your username/name to? (y/n)")
        if confirm.strip().lower() == "y":
          break
        name = str(input("> Enter your new username/name: "))
      checkLoggedIn()[1]["Name"] = name
      json.dump(accounts, open("data.json", "w"), indent=2)
      input(f"| Nice, your username is now '{checkLoggedIn()[1]['Name']}'.")


  elif settings == 2:
    if name == "Guest":
      about()
    else:
      heading("Menu > Settings > Delete Account")
      erase = input(
        f"[!] By {Fore.RED}deleting{Fore.WHITE} your account, {Fore.LIGHTYELLOW_EX}your name, list of shows, what your currently watching, and completed shows{Fore.WHITE} will be {Fore.LIGHTRED_EX}wiped{Fore.WHITE}. TL;DR: Data will be {Fore.LIGHTYELLOW_EX}unrecoverable{Fore.WHITE}. Are you sure you want to continue?\n"
        "[1] Erase.\n"
        "[2] On second thought...\n"
        ">>> "
        )
      try:
        erase = int(erase)
      except ValueError:
        input("[X] Invalid input, please try again!")
      if erase == 1:
        confirm = str(input(f"[{Fore.RED}!!!{Fore.WHITE}] Final warning: Are you positive that you want to {Fore.LIGHTRED_EX}erase ALL data completely{Fore.WHITE}? This cannot be {Fore.LIGHTYELLOW_EX}undone{Fore.WHITE}. (y/n)"))
        if confirm.strip().lower() == "y":
          accounts.remove(checkLoggedIn()[1])
          json.dump(accounts, open("data.json", "w"), indent=2)
          print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Data erased successfully.")
          advance = str(input(f"[.] In order to continue using this program, you'll need to {Fore.LIGHTYELLOW_EX}create a new account{Fore.WHITE}, or use {Fore.LIGHTYELLOW_EX}Guest Mode{Fore.WHITE}. If you want to later, type 'exit', if you want to now, type 'new'. (new/exit) "))
          if advance.strip().lower() == "new":
            welcome()
          else:
            sys.exit(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Closed.")
  elif settings == 3:
    if name != "Guest":
      heading("Menu > Settings > Sign Out")
      confirm = str(input("[?] Are you sure you want to sign out? (y/n)"))
      if confirm.strip().lower() == "y":
        for a in accounts:
          if a["Logged In"]:
            a["Logged In"] = False
            break
        print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Successfully signed out.")
        name = "Guest"
        json.dump(accounts, open("data.json", "w"), indent=2)
        welcome()
    else:
      searchSettings()
  elif settings == 4:
    if name != "Guest":
      about()
  elif settings == 5:
    if name != "Guest":
      searchSettings()
      json.dump(accounts, open("data.json", "w"), indent=2)


def searchShows():
  global selectedSearchedShow
  heading("Menu > Search")
  show = str(input("[?] What title are you looking for? (e to exit) "))
  if show.strip().lower() == "e":
    return
  print("[!] Searching... [This may take a while.]")
  if not findShow(show):
    return
  else:
    print("| Add [a] | Search Again [s] | Exit [e]")
    action = str(input(">>> "))
    if action.strip().lower() == "a":
      episode = int(input("[.] Enter the episode where you want to start watching: "))
      saveLocation = str(input("[?] Where would you like to save this to? (watchingNow/watchingLater/both) "))

      while saveLocation.strip().lower() not in ["watchingnow", "watchinglater", "both"]:
        input("[X] Invalid option. Please try again.")
        saveLocation = str(input("[?] Where would you like to save this to? (watchingNow/watchingLater/both) "))
      if checkShow(selectedSearchedShow, saveLocation.strip().lower()):
        return
      addNewShow(selectedSearchedShow, episode, location=saveLocation.strip().lower())
      selectedSearchedShow = None
      print(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Process complete.")
    elif action.strip().lower() == "s":
      searchShows()
      return

def feedback():
  heading("Menu > Feedback")
  print(
    "* If you have feedback about the program, whether it's about something that can be improved or a bug that should be fixed, please send it to the Github page.\n"
    f"-> Github Page: {Fore.LIGHTYELLOW_EX}https://www.github.com/MarkE16/ShowList{Fore.WHITE}"
  )
  input("Press ENTER to return to the menu. |")

def main():
  global name, selectedSearchedShow, accounts


  try:
    accounts = json.load(open("data.json", "r"))
  except:
    print("[.] Some data didn't load.")
  if not showList.authenticated():
    print(f"{Fore.RED}[!] You're not authenticated. It's not required, but it's HIGHLY recommended that you do so to increase Github's rate limit. Visit the Github page for more info on how to authenticate. -> https://www.github.com/MarkE16/ShowList")

  if not checkLoggedIn():
    welcome()
  else:
    name = checkLoggedIn()[1]["Name"]

  check_time(name)
  while True:
    print(
      "------------------------------------------\n"
      "[1] Your Upcoming Titles.\n"
      "[2] Titles You're Watching.\n"
      "[3] Your Completed Titles.\n"
      "[4] Search Titles.\n"
      "[5] Settings.\n"
      "[6] Submit Feedback.\n"
      "[7] Close.\n"
      "------------------------------------------"
    )
    action = input(">>> ")
    try:
      action = int(action)
    except ValueError:
      input("[X] Invalid input, please try again!")

    if action == 1:
      listOfShows()
    elif action == 2:
      watching()
    elif action == 3:
      completed()
    elif action == 4:
      searchShows()
    elif action == 5:
      userSettings()
    elif action == 6:
      feedback()
    elif action == 7:
      if name == "Guest":
        warning = str(input(f"[{Fore.RED}!{Fore.WHITE}] You're in {Fore.LIGHTYELLOW_EX}Guest Mode{Fore.WHITE}, and by exiting your data will be {Fore.LIGHTRED_EX}lost{Fore.WHITE}. Be sure to write down your shows somewhere else before exiting. Otherwise, do you really want to exit? (y/n)"))
        if warning.strip().lower() == "y":
          sys.exit(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Closed.")
      else:
        sys.exit(f"[{Fore.LIGHTGREEN_EX}√{Fore.WHITE}] Closed.")



if __name__ == "__main__":
  main()
