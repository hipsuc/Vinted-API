import requests
import json
from typing import Tuple, Union, Any

user_agent = {
    "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 14816.131.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

class VintedApi:

  def __init__(self, proxy=None) -> None:
    # Initializing session to get cookies
    self.session = requests.Session()
    if proxy:
      self.session.proxies.update(proxy)
    self.session.get("https://vinted.fr", headers=user_agent)


  def getProduct(self, id: int) -> Any:
    """
    Retrieving product informations

    Parameters
    ----------
    id: product id of the item. It can be found in the URL of the product.

    Returns
    ----------
    Return informations associated to a product if the request has been successful.
    Else, it will return the error.
    """

    # Adding this to translate to the detected browsing language
    params = {
        "localize": "true",
    }
    get_product = self.session.get(f"https://www.vinted.fr/api/v2/items/{id}", 
                                   headers=user_agent, params=params)
    if get_product.ok:
      json_product = json.loads(get_product.text)
      if json_product["code"] == 0:
        return json_product["item"]
      else:
        return json_product["message_code"]
    elif get_product.status_code == 429:
      return "Rate limited"
    else:
      return get_product


  def searchProducts(self, search_text: str, catalog_ids="", color_ids="",
                   brand_ids="", size_ids="", material_ids="",
                   video_game_rating_ids="", status_ids="", is_for_swap=0,
                   page=1, per_page=24, price_from="", price_to="", 
                   currency="EUR", order="newest_first") -> Any:
    """
    Searching products with filters

    Parameters
    ----------
    search_text: keyword that you want to search
    catalog_ids: ids of the sections (men, women...) format : id1,id2,id3
    color_ids: ids of the colors | format : id1,id2,id3
    sizes_ids: ids of the sizes | format : id1,id2,id3
    material_ids: ids of the materials | format : id1,id2,id3
    video_game_rating_ids: ids of the video game ratings | format : id1,id2,id3
    is_for_swap: 0 if false, 1 if true
    page: the page number you want to choose
    per_page: number of articles per page
    price_from: minimal price
    price_to: maximal price
    currency: currency you want to choose to filter the price
    order: how you want to filter out your data

    Returns
    ----------
    Return products matching the search if the request has been successful.
    Else, it will return the error.
    """

    params = {
        "search_text": search_text,
        "catalog_ids": catalog_ids,
        "color_ids": color_ids,
        "size_ids": size_ids,
        "material_ids": material_ids,
        "video_game_rating_ids": video_game_rating_ids,
        "is_for_swap": is_for_swap,
        "page": page,
        "per_page": per_page,
        "price_from": price_from,
        "price_to": price_to,
        "currency": currency,
        "order": order,
    }

    search_products = self.session.get("https://www.vinted.fr/api/v2/catalog/items",
                                  headers=user_agent, params=params)
    if search_products.ok:
      json_search = json.loads(search_products.text)
      if json_search["code"] == 0:
        return json_search["items"]
      else:
        return json_search["message_code"]
    elif search_products.status_code == 429:
      return "Rate limited"
    else:
      return search_products


  def getMember(self, member: Union[int, str]) -> Any:
    """
    Retrieving member informations

    Parameters
    ----------
    member: Can be the unique member id, passes as an int. It can also be the
    member name passes as a string.

    Returns
    ----------
    Return informations associated to a member if the request has been successful.
    Else, it will return the error.
    """
    get_member = self.session.get(f"https://www.vinted.fr/api/v2/users/{member}",
                                  headers=user_agent)
    if get_member.ok:
      json_member = json.loads(get_member.text)
      if json_member["code"] == 0:
        return json_member["user"]
      else:
        return json_member["message_code"]
    elif get_member.status_code == 429:
      return"Rate limited"
    else:
      return get_member

  
  def getMemberItems(self, member_id: int, order="relevance", page=1,
                     per_page=20) -> Any:
    """
    Retrieving member items

    Parameters
    ----------
    member_id: Unique member id. It can be found in the URL of a Vinted member
    order: how you want to filter out your data
    page: the page number you want to choose
    per_page: number of articles per page

    Returns
    ----------
    Return items of a member if the request has been successful.
    Else, it will return the error.
    """
    params = {
        "order": order,
        "page": page,
        "per_page": per_page,
    }

    get_member_items = self.session.get(f"https://www.vinted.fr/api/v2/users/{member_id}/items",
                                  headers=user_agent, params=params)
    if get_member_items.ok:
      json_member_items = json.loads(get_member_items.text)
      if json_member_items["code"] == 0:
        return json_member_items["items"]
      else:
        return json_member_items["message_code"]
    elif get_member_items.status_code == 429:
      return "Rate limited"
    else:
      return get_member_items


  def getMemberFeedbacks(self, member: Union[int, str], page=1, per_page=20) -> Any:
    """
    Retrieving member feedbacks

    Parameters
    ----------
    member: Can be the unique member id, passes as an int. It can also be the
    member name passes as a string.
    page: the page number you want to choose
    per_page: number of feedbacks per page

    Returns
    ----------
    Return feedbacks associated to a member if the request has been successful.
    Else, it will return the error.
    """
    params = {
      "user_id": member,
      "page": page,
      "per_page": per_page,
    }

    get_member_feedbacks = self.session.get(f"https://www.vinted.fr/api/v2/feedbacks",
                                            headers=user_agent, params=params)
    if get_member_feedbacks.ok:
      json_feedbacks = json.loads(get_member_feedbacks.text)
      if json_feedbacks["code"] == 0:
        return json_feedbacks["user_feedbacks"]
      else:
        return json_feedbacks["message_code"]
    elif get_member_feedbacks.status_code == 429:
      return "Rate limited"
    else:
      return get_member_feedbacks