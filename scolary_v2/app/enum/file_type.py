from enum import Enum


class FileTypeEnum(str, Enum):
  IMAGE = "image"
  VIDEO = "video"
  AUDIO = "audio"
  DOCUMENT = "document"
  OTHER = "other"
