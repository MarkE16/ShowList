import json
import imdb, github
from datetime import datetime
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
    # self.bs = bs4.BeautifulSoup
    self.upcoming: list = []
    self.watching: list = []
    self.completed: list = []
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
      # print(requests.get(f"https://www.imdb.com/find?q={title}&ref_=nv_sr_sm").text)
      # return [show for show in requests.get(f"https://v2.sg.media-imdb.com/suggests/{title[0]}/{title}.json").json().get("d")]
      # print()

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
      return self.ia.search_movie(queryName)[0].movieID
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
    info: dict = self.ia.get_movie(titleID)
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
        return self.ia.get_movie_episodes(titleID)['data']['number of episodes']
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
