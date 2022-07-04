import imdb, github, colorama
from datetime import datetime
from colorama import Fore
from auth import *
from time import time

# Create a function that calculates the execution time of a function
def time_execution(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"Execution time: {round(end - start, 2)} seconds")
        return result
    return wrapper

class ShowList():
  """
  The ShowList class.

  This class contains methods that can be useful for show tracking.
  """

  # DO NOT EDIT ANY OF THE FOLLOWING CODE UNLESS YOU KNOW WHAT YOU ARE DOING. ~ Mark

  def __init__(self) -> None:
    self.__version__ = "v1.3"
    self.__moduleversion__ = "v1.0.0"
    self.__programname__ = "Show List"
    self.__author__ = "Mark E"
    self.__description__ = "A program that allows you to keep track of shows you're watching."
    self.__copyright__ = "Copyright (c) 2021-2022 Mark E"
    self.ia = imdb.IMDb()
    self.github = github.Github() if TOKEN == "TOKEN" else github.Github(TOKEN)
    colorama.init(autoreset=True)
  
  @time_execution
  def search_show(self, title: str, limit:int=10) -> list:
    """
    search show method. This method will search the IMDB database for a show.
    If existing shows are found, the method will return a list of shows corresponding to the search.
    :param title: The title of the show to be searched for.
    :return: A list of shows corresponding to the search.
    """
    if isinstance(title, str):
      return [show for show in self.ia.search_movie(title, limit)]
    else:
      raise TypeError("Parameter 'title' must be string.")

  @time_execution
  def remove_show(self, item: str | int, target: list | dict) -> int | None:
    """
    Remove show method. This method will remove a show (item) from a list/dict (target).
    :param item: The show to be removed.
    :param target: The list/dict to be removed from.
    :return: None 
    """
    if isinstance(target, (list, dict)):
      if isinstance(item, int):
        target.pop(item)
        return 1
      if (item not in target) or (item != target):
        return None
      target.pop(item)
    else:
      raise TypeError("Parameter 'target' must be list or dict.")
    return None
  
  @time_execution
  def add_show(self, item: str | int, target: list | dict) -> int | None:
    """
    Add show method. This method will add a show (item) to a list/dict (target).
    :param item: The show to be added.
    :param target: The list/dict to be added to.
    :return: 1 if the item was added, 0 if the item was not added.
    """
    if isinstance(target, (list, dict)):
      if isinstance(target, list):
        if item in target:
          return None
        target.append(item)
      elif isinstance(target, dict):
        if (item in target) or (item == target):
          return None
        target = item
    else:
      raise TypeError("Parameter 'target' must be list or dict.")
    return None

  @time_execution
  def up_to_date(self) -> bool | tuple | str:
    """
    up_to_date method. This method will check if the current version of the program is up to date.
    :return: True if the program is up to date, False if it is not, and the version number of the latest version if it is not up to date as a tuple.
    """
    ver = self.github.get_repo("MarkE16/ShowList").get_latest_release().tag_name

    if "dev" in self.__version__:
      return f"\r{Fore.RED}[DEV] This is currently the development version of {self.__version__[:len(self.__version__)-4]}, which is not yet ready for release, which ALSO technically means that, you're up to date.{Fore.WHITE}"
    elif self.__version__ == ver:
      return True
    return (False, ver)
  
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
  def get_show_info(self, show:str | int, data="all") -> dict | list | str | int:
    """
    get_show_info method. This method will get the IMDB information for a show.
    :param show: The show to get the information for.
    :param data: The data to get. (types: all [default], title, year, rating, etc.)
    :return: The data requested.
    """
    if isinstance(show, str):
      showID = self.search_show(show)[0].movieID
      info = self.ia.get_movie(showID)
    elif isinstance(show, int):
      info = self.ia.get_movie(show)
    else:
      raise TypeError("Parameter 'show' must be string or int.")
    match data:
      case "all":
        return info
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
        return self.ia.get_movie_episodes(info.movieID)['data']['number of episodes']
      case "seasons":
        if info['kind'] == 'movie':
          raise TypeError("Title must be 'tv series' to get the number of seasons, not 'movie'.")
        return info['number of seasons']
      case "runtime":
        pass
      case "url":
        return self.ia.get_imdbURL(info)
  
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