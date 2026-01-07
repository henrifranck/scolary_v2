from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from app.core.config import settings


_client: Optional[MongoClient] = None


def get_mongo_client() -> Optional[MongoClient]:
  global _client
  if _client:
    return _client
  uri = settings.mongo_uri
  if not uri:
    return None
  try:
    _client = MongoClient(uri)
  except Exception:
    _client = None
  return _client


def get_notifications_collection() -> Optional[Collection]:
  client = get_mongo_client()
  if not client or not settings.MONGO_DATABASE:
    return None
  return client[settings.MONGO_DATABASE].get_collection("notifications")
