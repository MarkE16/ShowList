import json, sys, datetime, colorama
import os
from random import randint
from time import sleep, time
from showlist import ShowList
from tabulate import tabulate
from colorama import Fore
from auth import *
from imdb._exceptions import IMDbDataAccessError


def timeex(func):
  def wrapper(*args, **kwargs):
    start = time()
    result = func(*args, **kwargs)
    end = time()
    print(f"Execution time: {round(end - start, 2)} seconds")
    return result

  return wrapper


clear = lambda: os.system("cls")

episodes: int | None
seasons: int | None
runtime: int | None
hrs: float | None
mins: int | None
showList = ShowList()  # Initialize the Show List class
statuses = ["Upcoming", "Watching", "Complete", "Paused", "Dropped", "Uncertain", "Waiting"]
colorama.init(autoreset=True)


def heading(txt: str) -> None:
  print(f"{Fore.LIGHTBLUE_EX}{'-' * 40} {txt} {'-' * 40}")


def subheading(txt: str) -> None:
  print(f"{Fore.LIGHTBLUE_EX}{'-' * 40} {txt} {'-' * 40}")


def printMsg(msg: str, type: str = "success"):
  if type == "success":
    print(f"[{Fore.LIGHTGREEN_EX}SUCCESS{Fore.RESET}] {msg}")
  elif type == "error":
    print(f"[{Fore.LIGHTRED_EX}ERROR{Fore.RESET}] {msg}")
  elif type == "warning":
    print(f"[{Fore.LIGHTYELLOW_EX}WARNING{Fore.RESET}] {msg}")
  elif type == "info":
    print(f"[{Fore.LIGHTBLUE_EX}INFO{Fore.RESET}] {msg}")


def intro() -> None:
  heading("Welcome to Show List")
  print(
    f"This is the new and improved version of {Fore.LIGHTBLUE_EX}Show List{Fore.RESET}, with the current version being {showList.__version__}.\n"
    f"This version of Show List makes heavy improvements to the source code than the previous versions, and adds new features.\n"
    f"Please note that while this version is improved, it is {Fore.LIGHTRED_EX}HIGHLY LIKELY{Fore.RESET} that there are still bugs.\n"
    f"If you find any bugs, please report them to the GitHub repository here either through an issue or a pull request: => https://github.com/MarkE16/ShowList\n"
    f"With that out of the way, welcome.\n"
  )


def getInput(dataType: str | int | float | bool, msg: str) -> str | int | float | bool:
  match dataType:
    case "str":
      return str(input(msg))
    case "int":
      try:
        return int(input(msg))
      except ValueError:
        printMsg("Error: Invalid input. Please enter a valid integer.", "error")
        return -1
    case "float":
      try:
        return float(input(msg))
      except ValueError:
        printMsg("Error: Invalid input. Please enter a valid float.", "error")
        return -1
    case "bool":
      try:
        return bool(input(msg))
      except ValueError:
        printMsg("Error: Invalid input. Please enter a valid boolean.", "error")
        return -1
    case _:
      raise TypeError("Invalid data type.")
  # if dataType == "str":
  #   return str(input(msg))
  # elif dataType == "int":
  #   return int(input(msg))
  # elif dataType == "float":
  #   return float(input(msg))
  # elif dataType == "bool":
  #   return bool(input(msg))
  # else:
  #   raise TypeError("Invalid data type.")


def displayData(id: str) -> None:
  global hrs, seasons, mins, episodes
  try:
    data: dict = showList.get_show_info(id)['data']
  except IMDbDataAccessError as e:
    printMsg("Error: Unable to connect to IMDb. ERR: " + str({"error": e}), "error")
    return
  dataKeys = data.keys()
  upcomingTitles: list = [title['title'] for title in showList.upcoming]
  watchingTitles: list = [title['title'] for title in showList.watching]
  completedTitles: list = [title['title'] for title in showList.completed]
  index: int = 0
  inList: str = f"{Fore.LIGHTGREEN_EX}√{Fore.RESET}"
  notInList: str = f"{Fore.LIGHTRED_EX}X{Fore.RESET}"
  if data['kind'] == "tv series":
    episodes = showList.get_show_info(id, "episodes")
    seasons = data['number of seasons'] if 'number of seasons' in dataKeys else None
    runtime = None
    hrs = None
    mins = None
  else:
    if "runtimes" in dataKeys:
      runtime = int(data['runtimes'][0])
      hrs = runtime / 60
      mins = runtime - (int(hrs) * 60)
      episodes = None
      seasons = None
  # ---
  if data['title'] in watchingTitles:
    index = watchingTitles.index(data['title'])

  subheading("Title information")
  print(
    f"{Fore.LIGHTBLUE_EX}Title:{Fore.RESET} {data['title']}\n"
    f"{Fore.LIGHTBLUE_EX}Title Type:{Fore.RESET} {data['kind'].capitalize()}\n"
    f"{Fore.LIGHTBLUE_EX}Year:{Fore.RESET} {data['year']}"
  )
  print(f"{Fore.LIGHTBLUE_EX}Episodes:{Fore.RESET} {episodes} | {Fore.LIGHTBLUE_EX}Seasons:{Fore.RESET} {seasons}" + (f" | {Fore.LIGHTBLUE_EX}On Episode:{Fore.RESET} {showList.watching[index]['ep']}" if data['title'] in watchingTitles else "")
        if data['kind'] == "tv series" else f"{Fore.LIGHTBLUE_EX}Runtime:{Fore.RESET} {int(hrs)} hour(s) and {mins} minutes"if "runtimes" in dataKeys else f"{Fore.LIGHTBLUE_EX}Runtime:{Fore.RESET} No Data Available.")
  print(
    f"{Fore.LIGHTBLUE_EX}Rating:{Fore.RESET} {data['rating'] if 'rating' in dataKeys else '?'}/10\n"
    f"{Fore.LIGHTBLUE_EX}Genres:{Fore.RESET} {[genre for genre in data['genres']] if 'genres' in dataKeys else 'No Genres Listed.'}\n"
    f"{Fore.LIGHTBLUE_EX}Plot:{Fore.RESET} {data['plot'][0] if 'plot' in dataKeys else 'No Plot Available.'}\n"
  )
  print(f"[{inList if data['title'] in upcomingTitles else notInList}] Upcoming | [{inList if data['title'] in watchingTitles else notInList}] Watching | [{inList if data['title'] in completedTitles else notInList}] Complete")


def searchTitle() -> None:
  subheading("Search a title")
  name: str = getInput("str", "Enter the title to search for: ")
  clear()
  subheading("Search results")
  try:
    results: list = showList.search_show(name, showList.searchLimit)
  except IMDbDataAccessError as e:
    printMsg("Error: Unable to connect to IMDb. ERR: " + str({"error": e}), "error")
    return
  if len(results) == 0:
    printMsg("No results found. Try checking for any typos. Example searches: 'Spiderman', 'Demon Slayer', 'Cars'", "warning")
    return
  for index, title in enumerate(results):
    print(f"{Fore.LIGHTBLUE_EX}[{index}]{Fore.RESET} {title['long imdb canonical title']}")
  print()
  printMsg("Results displayed: " + str(len(results)) + "/" + str(showList.searchLimit), "info")
  selected: int = getInput("int", "Select a title to view more information: ")
  titleID: str = showList.getTitleID(results[selected]["long imdb canonical title"])
  print()
  displayData(titleID)
  print("| [0] Add to list | [1] Go back |")
  action: int = getInput("int", "Select an action: ")
  if action == 1:
    clear()
    return
  elif action == 0:
    clear()
    subheading("Add to list")
    print(
      f"Where you do want to add '{Fore.LIGHTYELLOW_EX}{results[selected]['long imdb canonical title']}{Fore.RESET}' to?")
    print("[0] Upcoming | [1] Watching | [2] Complete | [3] Back |")
    action: int = getInput("int", "Select an action: ")
    if action == 3:
      clear()
      return
    elif action == 0:
      try:
        showList.add_title(results[selected]['title'], "upcoming")
      except ValueError:
        printMsg("Error: Title already exists in list.", "error")
        return
    elif action == 1:
      try:
        showList.add_title(results[selected]['title'], "watching")
      except ValueError:
        printMsg("Error: Title already exists in list.", "error")
        return
    elif action == 2:
      try:
        showList.add_title(results[selected]['title'], "completed")
      except ValueError:
        printMsg("Error: Title already exists in list.", "error")
        return
    printMsg("Successfully added title to list.", "success")


def viewList(l: str) -> int:
  clear()
  if l == "upcoming":
    print(tabulate(showList.upcoming, headers="keys", tablefmt="fancy_grid", showindex="always"))
  elif l == "watching":
    print(tabulate(showList.watching, headers="keys", tablefmt="fancy_grid", showindex="always"))
  elif l == "complete":
    print(tabulate(showList.completed, headers="keys", tablefmt="fancy_grid", showindex="always"))
  print()
  return getInput("int", "Select a title: ")

def changeEpisode(l: str, index: int) -> None:
  newEpisode: int = getInput("int", "Enter the new episode: ")
  confirm: str = getInput("str",
                          "Are you sure you want to change the current episode to '" + str(newEpisode) + "'? [y/n]: ")
  while confirm != "y" or (confirm != "n" and confirm != "y"):
    newEpisode: int = getInput("int", "Enter the new episode: ")
    confirm = getInput("str",
                       "Are you sure you want to change the current episode to '" + str(newEpisode) + "'? [y/n]: ")
  if confirm == "y":
    if l == "upcoming":
      showList.upcoming[index]['ep'] = newEpisode
    elif l == "watching":
      showList.watching[index]['ep'] = newEpisode
    elif l == "complete":
      showList.completed[index]['ep'] = newEpisode
    printMsg("Successfully changed current episode.", "success")
    return
  elif confirm == "n":
    return


def changeStatus(l: str, index: int) -> None:
  print("Statuses: " + str(statuses))
  newStatus: str = getInput("str", "Enter the new status (e.g the name. Not case-sensitive): ")
  if newStatus.capitalize() not in statuses:
    printMsg("Invalid status.", "error")
    return
  elif newStatus.capitalize() == showList.upcoming[index]['status']:
    printMsg("That is already the status.", "error")
    return
  if l == "upcoming":
    showList.upcoming[index]['status'] = newStatus.capitalize()
  elif l == "watching":
    showList.watching[index]['status'] = newStatus.capitalize()
  elif l == "complete":
    showList.completed[index]['status'] = newStatus.capitalize()
  printMsg("Successfully changed status.", "success")


def viewUpcoming() -> None:
  if not showList.upcoming:
    printMsg("You have no upcoming titles. Add some titles, and they will appear here.", "error")
    return
  subheading("Upcoming shows")
  print()
  print(tabulate(showList.upcoming, headers="keys", tablefmt="fancy_grid", showindex="always"))
  print()
  print("[0] View title | [1] Remove title | [2] Move title | [3] Edit title | [4] Back |")
  action: int = getInput("int", "Select an action: ")
  if action == 4:
    clear()
    return
  selectedTitleIndex: int = viewList("upcoming")
  if selectedTitleIndex >= len(showList.upcoming) or selectedTitleIndex < 0:
    printMsg("Invalid index.", "error")
    return
  if action == 0:
    clear()
    displayData(showList.getTitleID(showList.upcoming[selectedTitleIndex]['title']))
    input("[ENTER] Back |")
    clear()
    return
  elif action == 1:
    clear()
    subheading("Remove title")
    print(f"Are you sure you want to remove '{Fore.LIGHTYELLOW_EX}{showList.upcoming[selectedTitleIndex]['title']}{Fore.RESET}' from your upcoming list?")
    print(f"[0] {Fore.LIGHTRED_EX}Yes{Fore.RESET} | [1] No |")
    action: int = getInput("int", "Select an action: ")
    if action == 1:
      clear()
      return
    elif action == 0:
      showList.remove_title(showList.upcoming[selectedTitleIndex], "upcoming")
      printMsg("Successfully removed title from list.", "success")
      return
  elif action == 2:
    clear()
    subheading("Move title")
    print(f"Where you do want to move '{Fore.LIGHTYELLOW_EX}{showList.upcoming[selectedTitleIndex]['title']}{Fore.RESET}' to?")
    print("[0] Watching | [1] Complete | [2] Back |")
    action: int = getInput("int", "Select an action: ")
    if action == 2 or action == -1:
      return
    elif action == 0:
      showList.add_title(showList.upcoming[selectedTitleIndex]['title'], "watching")
      showList.remove_title(showList.upcoming[selectedTitleIndex], "upcoming")
    elif action == 1:
      showList.add_title(showList.upcoming[selectedTitleIndex]['title'], "completed")
      showList.remove_title(showList.upcoming[selectedTitleIndex], "upcoming")
    printMsg("Successfully moved title.", "success")
    return
  elif action == 3:
    clear()
    subheading("Edit Title")
    print(f"What do you want to edit for '{Fore.LIGHTYELLOW_EX}{showList.upcoming[selectedTitleIndex]['title']}{Fore.RESET}'?")
    print("[0] Current Episode | [1] Status | [2] Back |")
    action: int = getInput("int", "Select an action: ")
    if action == 2 or action == -1:
      return
    elif action == 0:
      changeEpisode("upcoming", selectedTitleIndex)
    elif action == 1:
      changeStatus("upcoming", selectedTitleIndex)


def viewWatching() -> None:
  if not showList.watching:
    printMsg("You have no shows in your watching list. Add some titles, and they will appear here.", "error")
    return
  subheading("Watching shows")
  print()
  print(tabulate(showList.watching, headers="keys", tablefmt="fancy_grid", showindex="always"))
  print()
  print("[0] View title | [1] Remove title | [2] Move title | [3] Edit title | [4] Back |")
  action: int = getInput("int", "Select an action: ")
  if action == 4:
    clear()
    return
  selectedTitleIndex: int = viewList("watching")
  if selectedTitleIndex >= len(showList.watching) or selectedTitleIndex < 0:
    printMsg("Invalid index.", "error")
    return
  if action == 0:
    clear()
    subheading("Title information")
    displayData(showList.getTitleID(showList.watching[selectedTitleIndex]['title']))
    input("[ENTER] Back |")
    clear()
    return
  elif action == 1:
    clear()
    subheading("Remove title")
    print(f"Are you sure you want to remove '{Fore.LIGHTYELLOW_EX}{showList.watching[selectedTitleIndex]['title']}{Fore.RESET}' from your watching list?")
    print(f"[0] {Fore.LIGHTRED_EX}Yes{Fore.RESET} | [1] No |")
    action: int = getInput("int", "Select an action: ")
    if action == 1:
      clear()
      return
    elif action == 0:
      showList.remove_title(showList.watching[selectedTitleIndex], "watching")
      printMsg("Successfully removed title from list.", "success")
      return
  elif action == 2:
    clear()
    subheading("Move title")
    print(f"Where you do want to move '{Fore.LIGHTYELLOW_EX}{showList.watching[selectedTitleIndex]['title']}{Fore.RESET}' to?")
    print("[0] Upcoming | [1] Complete | [2] Back |")
    action: int = getInput("int", "Select an action: ")
    if action == 2 or action == -1:
      return
    elif action == 0:
      showList.add_title(showList.watching[selectedTitleIndex]['title'], "upcoming")
      showList.remove_title(showList.watching[selectedTitleIndex], "watching")
    elif action == 1:
      showList.add_title(showList.watching[selectedTitleIndex]['title'], "completed")
      showList.remove_title(showList.watching[selectedTitleIndex], "watching")
    printMsg("Successfully moved title.", "success")
    return
  elif action == 3:
    clear()
    subheading("Edit Title")
    print(f"What do you want to edit for '{Fore.LIGHTYELLOW_EX}{showList.watching[selectedTitleIndex]['title']}{Fore.RESET}'?")
    print("[0] Current Episode | [1] Status | [2] Back |")
    action: int = getInput("int", "Select an action: ")
    if action == 2 or action == -1:
      return
    elif action == 0:
      changeEpisode("watching", selectedTitleIndex)
    elif action == 1:
      changeStatus("watching", selectedTitleIndex)


def viewComplete() -> None:
  if not showList.completed:
    printMsg("You have no shows in your complete list. Add some titles, and they will appear here.", "error")
    return
  subheading("Complete shows")
  print()
  print(tabulate(showList.completed, headers="keys", tablefmt="fancy_grid", showindex="always"))
  print()
  print("[0] View title | [1] Remove title | [2] Move title | [3] Back |")
  action: int = getInput("int", "Select an action: ")
  if action == 3:
    clear()
    return
  selectedTitleIndex: int = viewList("complete")
  if selectedTitleIndex >= len(showList.completed) or selectedTitleIndex < 0:
    printMsg("Invalid index.", "error")
    return
  if action == 0:
    clear()
    subheading("Title information")
    displayData(showList.getTitleID(showList.completed[selectedTitleIndex]['title']))
    input("[ENTER] Back |")
    clear()
    return
  elif action == 1:
    clear()
    subheading("Remove title")
    print(f"Are you sure you want to remove '{Fore.LIGHTYELLOW_EX}{showList.completed[selectedTitleIndex]['title']}{Fore.RESET}' from your complete list?")
    print(f"[0] {Fore.LIGHTRED_EX}Yes{Fore.RESET} | [1] No |")
    action: int = getInput("int", "Select an action: ")
    if action == 1:
      clear()
      return
    elif action == 0:
      showList.remove_title(showList.completed[selectedTitleIndex], "completed")
      printMsg("Successfully removed title from list.", "success")
      return
  elif action == 2:
    clear()
    subheading("Move title")
    print(f"Where you do want to move '{Fore.LIGHTYELLOW_EX}{showList.completed[selectedTitleIndex]}{Fore.RESET}' to?")
    print("[0] Upcoming | [1] Watching | [2] Back |")
    action: int = getInput("int", "Select an action: ")
    if action == 2 or action == -1:
      return
    elif action == 0:
      showList.add_title(showList.completed[selectedTitleIndex]['title'], "upcoming")
      showList.remove_title(showList.completed[selectedTitleIndex], "completed")
    elif action == 1:
      showList.add_title(showList.completed[selectedTitleIndex]['title'], "watching")
      showList.remove_title(showList.completed[selectedTitleIndex], "completed")
    printMsg("Successfully moved title.", "success")
    return



def checkForUpdates() -> None:
  clear()
  subheading("Check for updates")
  print()
  print("Checking for updates...")
  print()
  sleep(1)
  if showList.up_to_date() and isinstance(showList.up_to_date(), bool):
    printMsg("You are up to date! No further actions needed.", "success")
  elif not showList.up_to_date() and isinstance(showList.up_to_date(), bool):
    print(
      "\r========================================================\n"
      f"{Fore.LIGHTYELLOW_EX}/!\{Fore.WHITE} A {Fore.YELLOW}new version{Fore.WHITE} is available!\n"
      ">>> Current version: " + showList.__version__ + " | Latest version: " + showList.fetchLatestVersion() + "\n"
      f"\nYou can download the latest version from: https://www.github.com/MarkE16/ShowList\n{Fore.RED}Note: Save data will not transfer, so you'll need to go into program's files and make a copy of the"
      f" data.json file, then transfer it to the new version. More information about updating on the Github page.{Fore.WHITE}\n"
      "========================================================\n"
    )
  else:
    printMsg("An error occurred while checking for updates. Please try again later. ERR: " + str(showList.up_to_date()), "error")


def programInfo() -> None:
  subheading("Program information")
  print(
    f"{Fore.LIGHTBLUE_EX}Version:{Fore.RESET} {showList.__version__}\n"
    f"{Fore.LIGHTBLUE_EX}Author:{Fore.RESET} {showList.__author__}\n"
    f"{Fore.LIGHTBLUE_EX}Copyright: {Fore.RESET} {showList.__copyright__}\n"
    f"{Fore.LIGHTBLUE_EX}Repository:{Fore.RESET} {showList.__repo__}\n"
  )
  print("| [0] Check for updates | [1] Go back |")
  action: int = getInput("int", "Select an action: ")
  if action == 1:
    clear()
    return
  elif action == 0:
    checkForUpdates()


def settings() -> None:
  subheading("Settings")
  print(f"{Fore.LIGHTBLUE_EX}Search Limit:{Fore.RESET} {showList.searchLimit}")
  print(f"{Fore.LIGHTBLUE_EX}Hints:{Fore.RESET} {showList.hints}")
  print()
  print("[0] Change search limit | [1] Toggle hints | [2] Go back |")
  action: int = getInput("int", "Select an action: ")
  if action == 2:
    clear()
    return
  elif action == 0:
    limit: int = getInput("int", "Enter a new search limit: ")
    if limit < 1:
      printMsg("Invalid search limit.", "error")
      return
    showList.set_limit(limit)
    printMsg("Successfully changed search limit.", "success")
  elif action == 1:
    showList.toggle_hints()
    printMsg("Successfully toggled hints.", "success")

def mainMenu() -> None:
  try:
    showList.load()
  except FileNotFoundError:
    print("Failed to load data. The file 'data2.json' does not exist. Please create it in the root directory of the program.")
  while True:
    print(
      f"{Fore.LIGHTBLUE_EX}Select an option to get started{Fore.RESET}\n"
      f"{Fore.LIGHTBLUE_EX}[0]{Fore.RESET} Search a title - Find what you're interested in.\n"
      f"{Fore.LIGHTBLUE_EX}[1]{Fore.RESET} View Upcoming - View what you're planning to watch.\n"
      f"{Fore.LIGHTBLUE_EX}[2]{Fore.RESET} View Watching - View what you're currently watching.\n"
      f"{Fore.LIGHTBLUE_EX}[3]{Fore.RESET} View Completed - View what you've completed.\n"
      f"{Fore.LIGHTBLUE_EX}[4]{Fore.RESET} Program Information - Basic Information about the program.\n"
      f"{Fore.LIGHTBLUE_EX}[5]{Fore.RESET} Settings - Alter how the program functions.\n"
      f"{Fore.LIGHTBLUE_EX}[6]{Fore.RESET} Exit - Exit the program.\n"
    )
    action: int = getInput("int", "> ")
    if action == 0:
      searchTitle()
    elif action == 1:
      viewUpcoming()
    elif action == 2:
      viewWatching()
    elif action == 3:
      viewComplete()
    elif action == 4:
      programInfo()
    elif action == 5:
      settings()
    elif action == 6:
      exit(0)


def main() -> None:
  intro()
  print()
  mainMenu()


if __name__ == "__main__":
  main()
