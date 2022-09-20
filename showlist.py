import json
import imdb, github
from datetime import datetime

from imdb import IMDbDataAccessError
from imdb._exceptions import IMDbParserError

from auth import *
from time import time
from github.GithubException import BadCredentialsException, RateLimitExceededException

# Create a function that calculates the execution time of a function
def time_execution(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"Execution time: {round(end - start, 2)} seconds for function {func.__name__} | Parameters for this function: {args}")
        return result
    return wrapper

class ShowList():
  """
  The ShowList class.

  This class contains methods that can be useful for show tracking.
  """

  # DO NOT EDIT ANY OF THE FOLLOWING CODE UNLESS YOU KNOW WHAT YOU ARE DOING. ~ Mark

  def __init__(self) -> None:
    self.__version__ = "v2.0"
    self.__moduleversion__ = "v1.0.0"
    self.__programname__ = "Show List"
    self.__author__ = "Mark E"
    self.__description__ = "A program that allows you to keep track of shows you're watching."
    self.__copyright__ = "Copyright (c) 2021-2022 Mark E"
    self.__repo__ = "https://github.com/MarkE16/ShowList"
    self.ia = imdb.Cinemagoer()
    self.upcoming: list = []
    self.watching: list = []
    self.completed: list = []
    self.searchLimit = 10
    self.hints = True
    self.adult = False
    self.github = github.Github() if TOKEN == "TOKEN" else github.Github(TOKEN)

  def load(self) -> None:
    """
    load method. This method will load the data from the data file.
    :return: None
    """
    with open("data2.json", "r") as f:
      data = json.load(f)
      self.upcoming = data["upcoming"]
      self.watching = data["watching"]
      self.completed = data["completed"]
      self.searchLimit = data["settings"]["searchLimit"]
      self.hints = data["settings"]["hints"]
      self.adult = data["settings"]["adult"]


  def save(self) -> None:
    """
    save method. This method will save the data to the data file.
    :return: None
    """
    data = {
      "upcoming": self.upcoming,
      "watching": self.watching,
      "completed": self.completed,
      "settings": {
        "searchLimit": self.searchLimit,
        "hints": self.hints,
        "adult": self.adult
      }
    }
    with open("data2.json", "w") as f:
      json.dump(data, f, indent=2)


  def set_limit(self, newLimit: int) -> None:
    """
    set_limit method. This method will set the search limit.
    :param newLimit: The new search limit.
    :return: None
    """
    self.searchLimit = newLimit


  def toggle_hints(self) -> None:
    """
    toggle_hints method. This method will toggle the hints.
    :return: None
    """
    self.hints = not self.hints


  def toggle_adult(self) -> None:
    """
    toggle_adult method. This method will toggle the adult content.
    :return: None
    """
    self.adult = not self.adult


  @time_execution
  def search_show(self, title: str, limit:int=10) -> list:
    """
    search show method. This method will search the IMDB database for a show.
    If existing shows are found, the method will return a list of shows corresponding to the search.
    :param title: The title of the show to be searched for.
    :return: A list of shows corresponding to the search.
    """
    if isinstance(title, str):
      return [show for show in self.ia.search_movie_advanced(title, self.adult, limit)]
    else:
      raise TypeError("Parameter 'title' must be string.")

  #

  @time_execution
  def add_title(self, title: str | dict, titleList: str) -> None:
    """
    add_title method. This method will add a title to the specified list.
    :param title: The title to be added.
    :param titleList: The list to add the title to.
    :return: None
    """
    if titleList == "upcoming":
      if title in [show["title"] for show in self.upcoming]:
        raise ValueError("Title already exists in the list.")
      self.upcoming.append({"title": title, "ep": 1, "status": "Upcoming"})
    elif titleList == "watching":
      if title in [show["title"] for show in self.watching]:
        raise ValueError("Title already exists in the list.")
      self.watching.append({"title": title, "ep": 1, "status": "Watching"})
    elif titleList == "completed":
      if title in self.completed:
        raise ValueError("Title already exists in the list.")
      self.completed.append({"title": title})
    else:
      raise ValueError("Invalid title list.")
    self.save()

  @time_execution
  def remove_title(self, title: str | dict, titleList: str) -> None:
    """
    remove_title method. This method will remove a title from the specified list.
    :param title: The title to be removed.
    :param titleList: The list to remove the title from.
    :return: None
    """
    if titleList == "upcoming":
      self.upcoming.remove(title)
    elif titleList == "watching":
      self.watching.remove(title)
    elif titleList == "completed":
      self.completed.remove(title)
    else:
      raise ValueError("Invalid title list.")
    self.save()

  def update_title_info(self, l: str, index: int, type: str, newValue: str | int) -> None:
      """
      update_title_info method. This method will update the information of a title.
      :param l: The list to update the title in.
      :param index: The index of the title in the list.
      :param type: The type of information to update.
      :param newValue: The new value of the information.
      :return: None
      """
      if l == "upcoming":
          if type == "ep":
              self.upcoming[index]["ep"] = newValue
          elif type == "status":
              self.upcoming[index]["status"] = newValue
          else:
              raise ValueError("Invalid type.")
      elif l == "watching":
          if type == "ep":
              self.watching[index]["ep"] = newValue
          elif type == "status":
              self.watching[index]["status"] = newValue
          else:
              raise ValueError("Invalid type.")
      else:
          raise ValueError("Invalid list.")
      self.save()


  def fetchLatestVersion(self) -> str:
    """
    fetchLatestVersion method. This method will fetch the latest version of the program from GitHub.
    :return: The latest version of the program.
    """
    return self.github.get_repo("MarkE16/ShowList").get_latest_release().tag_name


  @time_execution
  def up_to_date(self) -> bool | dict:
    """
    up_to_date method. This method will check if the current version of the program is up to date.
    :return: True if the program is up-to-date, False if it is not, and the version number of the latest version if it is not up to date as a tuple.
    """
    try:
      ver = self.fetchLatestVersion()
    except BadCredentialsException:
      return {"error": "BadCredentialsException", "message": "The GitHub token is invalid."}


    if self.__version__ == ver:
      return True
    return False
  # Old Method, might be unused.
  # def update(self):
  #   """
  #   update method. This method will update the program to the latest version.
  #   """
  #   # Loading bar animation.
  #   #░█
  #   def loadbar(percent, width=50):
  #     if percent < 0:
  #       percent = 0
  #     elif percent > 100:
  #       percent = 100
  #     show_str = ('█' * int(round(percent / 100 * width)))
  #     hide_str = ('.' * (width - len(show_str)))
  #     print("\r[.] Updating... |{0}| {1}%".format(show_str + hide_str, int(percent)), end="")
    
  #   print("[!] The update will now begin. Do not close this window until the update is complete.")
  #   time.sleep(2)
  #   for i in range(os.path.getsize("main.py") + 1):
  #     loadbar(i / os.path.getsize("main.py") * 100, 30)
    
  #   self.__version__ = open("version.txt", "r").read()

  @time_execution
  def getTitleID(self, queryName: str) -> str:
    """
    getTitleID method. This method will return the ID of the first result that closely represents the given query title.
    :param queryName: The show to get the ID of.
    :return: The ID of the show.
    """
    if isinstance(queryName, str):
      try:
        return self.search_show(queryName)[0].movieID
      except IndexError:
        print("This is the error.")
        return ""
    else:
      raise TypeError("Parameter 'queryName' must be string.")

  @time_execution
  def get_show_info(self, titleID: str, data="all") -> dict | list | str | int:
    """
    get_show_info method. This method will get the IMDB information for a show.
    :param titleID: The show to get the information for.
    :param data: The data to get. (types: all[default], title, year, rating, etc.)
    :return: The data requested.
    """
    # if isinstance(show, str):
    #   showID = self.search_show(show)[0].movieID
    #   info = self.ia.get_movie(showID)
    # elif isinstance(show, int):
    #   info = self.ia.get_movie(show)
    # else:
    #   raise TypeError("Parameter 'show' must be string or int.")
    try:
      info: dict = self.ia.get_movie(titleID)
    except IMDbParserError:
      raise ValueError("Invalid title ID.")
    match data:
      case "all":
        return info.__dict__
      case "title":
        return info['title']
      case "kind":
        return info['kind']
      case "year":
        return info['year']
      case "rating":
        return info['rating']
      case "votes":
        return info['votes']
      case "genres":
        return info['genres']
      case "plot":
        return info['plot'][0]
      case "cast":
        return info['cast']
      case "episodes":
        try:
          return self.ia.get_movie_episodes(titleID)['data']['number of episodes']
        except KeyError:
          return "No episodes found."
        except IMDbDataAccessError:
          return "No episodes found."
      case "seasons":
        if info['kind'] == 'movie':
          raise TypeError("Title must be 'tv series' to get the number of seasons, not 'movie'.")
        return info['number of seasons']
      case "runtime":
        pass
      case "url":
        return self.ia.get_imdbURL(info)
    # if data == "all":
    #   return info.__dict__
    # elif data == "title":
    #   return info['title']
    # elif data == "kind":
    #   return info['kind']
    # elif data == "year":
    #   return info['year']
    # elif data == "rating":
    #   return info['rating']
    # elif data == "votes":
    #   return info['votes']
    # elif data == "genres":
    #   return info['genres']
    # elif data == "plot":
    #   return info['plot'][0]
    # elif data == "cast":
    #   return info['cast']
    # elif data == "episodes":
    #   return self.ia.get_movie_episodes(titleID)['data']['number of episodes']
    # elif data == "seasons":
    #   if info['kind'] == 'movie':
    #     raise TypeError("Title must be 'tv series' to get the number of seasons, not 'movie'.")
    #   return info['number of seasons']
    # elif data == "runtime":
    #   pass
    # elif data == "url":
    #   return self.ia.get_imdbURL(info)
  
  def authenticated(self) -> bool:
    """
    authenticated method. This method will check if the user is authenticated with the user's GitHub account.
    :return: True if the user is authenticated, False if not.
    """
    try:
      self.github.get_user().login
    except github.GithubException:
      return False
    return True
    
  
  def get_rate_limit_reset(self) -> str:
    """
    get_rate_limit_reset method. This method will get the reset time of the rate limit from GitHub.
    :return: The reset time of the rate limit.
    """
    refresh = self.github.rate_limiting_resettime

    return datetime.utcfromtimestamp(refresh).strftime('%Y/%m/%d %I:%M:%p UTC')
