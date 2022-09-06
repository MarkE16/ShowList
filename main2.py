import json, sys, datetime, colorama
import os
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


clear = lambda: os.system("cls")

guestShowsToWatch = []
guestShowsWatching = []
guestCompletedShows = []
guestSettings = {"MaxResults": 10, "PlotPreview": False}
accounts = []
increment = 0
selectedSearchedShow = None
showList = ShowList()  # Initialize the Show List class
statuses = ["Watching", "Complete", "Paused", "Dropped", "Uncertain", "Waiting"]
name: str = ""
colorama.init(autoreset=True)


def heading(txt: str) -> None:
  print(f"{Fore.LIGHTBLUE_EX}{'-' * 40} {txt} {'-' * 40}")


def subheading(txt: str) -> None:
  print(f"{Fore.LIGHTBLUE_EX}{'-' * 40} {txt} {'-' * 40}")


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
      return int(input(msg))
    case "float":
      return float(input(msg))
    case "bool":
      return bool(input(msg))
    case _:
      raise TypeError("Invalid data type.")

def displayData(data: list) -> None:
  # print(tabulate(data, tablefmt="fancy_grid"))
  print(data)

def searchTitle() -> None:
  subheading("Search a title")
  name: str = getInput("str", "Enter the title to search for: ")
  clear()
  subheading("Search results")
  results: list = showList.search_show(name, 10)
  # print(tabulate([title for title in results], headers="Title", tablefmt="fancy_grid"))
  for index, title in enumerate(results):
    print(f"{Fore.LIGHTBLUE_EX}[{index}]{Fore.RESET} {title['long imdb canonical title']}")
  print()
  action: int = getInput("int", "Select a title to view more information: ")
  titleID: str = showList.getTitleID(results[action]["long imdb canonical title"])
  info: dict = showList.ia.get_movie(titleID)
  print()
  print(displayData(info))


def mainMenu() -> None:
  while True:
    print(
      f"{Fore.LIGHTBLUE_EX}Select an option to get started{Fore.RESET}\n"
      f"{Fore.LIGHTBLUE_EX}[0]{Fore.RESET} Search a title\n"
    )
    action: int = getInput("int", "> ")
    if action == 0:
      searchTitle()


def main() -> None:
  intro()
  print()
  mainMenu()


if __name__ == "__main__":
  main()
