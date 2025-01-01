from bson.objectid import ObjectId

class Event:
    def __init__(self, ownerId, type, title, description, date, from_time, to_time, location, group, organizer, _id=None):
        self.ownerId = ownerId
        self.type = type
        self.title = title
        self.description = description
        self.date = date
        self.from_time = from_time
        self.to_time = to_time
        self.location = location
        self.group = group
        self.organizer = organizer
        self._id = str(_id) if _id else None

    def to_dict(self):
        event_dict = {
            "ownerId": self.ownerId,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "from": self.from_time,
            "to": self.to_time,
            "location": self.location,
            "group": self.group,
            "organizer": self.organizer
        }
        if self._id:
            event_dict["_id"] = self._id
        return event_dict

    @staticmethod
    def from_dict(data):
        return Event(
            ownerId=data.get("ownerId"),
            type=data.get("type"),
            title=data.get("title"),
            description=data.get("description"),
            date=data.get("date"),
            from_time=data.get("from"),
            to_time=data.get("to"),
            location=data.get("location"),
            group=data.get("group"),
            organizer=data.get("organizer"),
            _id=str(data.get("_id")) if data.get("_id") else None
        )