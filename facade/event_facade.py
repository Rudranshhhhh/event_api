import logging
from flask import current_app
from bson.objectid import ObjectId
from models.event import Event

class EventFacade:
    @staticmethod
    def create_event(ownerId, type, title, description, date, from_time, to_time, location, group, organizer):
        try:
            event = Event(
                ownerId=ownerId,
                type=type,
                title=title,
                description=description,
                date=date,
                from_time=from_time,
                to_time=to_time,
                location=location,
                group=group,
                organizer=organizer
            )
            result = current_app.mongo.db.events.insert_one(event.to_dict())
            event._id = str(result.inserted_id)
            return event.to_dict()
        except Exception as e:
            logging.error("Error creating event: %s", e)
            raise

    @staticmethod
    def get_event(event_id):
        try:
            event_data = current_app.mongo.db.events.find_one({"_id": ObjectId(event_id)})
            if event_data:
                event = Event.from_dict(event_data)
                return event.to_dict()
            return None
        except Exception as e:
            logging.error("Error getting event: %s", e)
            raise

    @staticmethod
    def update_event(event_id, ownerId=None, type=None, title=None, description=None, date=None, from_time=None, to_time=None, location=None, group=None, organizer=None):
        try:
            update_fields = {}
            if ownerId:
                update_fields["ownerId"] = ownerId
            if type:
                update_fields["type"] = type
            if title:
                update_fields["title"] = title
            if description:
                update_fields["description"] = description
            if date:
                update_fields["date"] = date
            if from_time:
                update_fields["from"] = from_time
            if to_time:
                update_fields["to"] = to_time
            if location:
                update_fields["location"] = location
            if group:
                update_fields["group"] = group
            if organizer:
                update_fields["organizer"] = organizer
            result = current_app.mongo.db.events.update_one(
                {"_id": ObjectId(event_id)}, {"$set": update_fields}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error("Error updating event: %s", e)
            raise

    @staticmethod
    def delete_event(event_id):
        try:
            result = current_app.mongo.db.events.delete_one({"_id": ObjectId(event_id)})
            return result.deleted_count > 0
        except Exception as e:
            logging.error("Error deleting event: %s", e)
            raise

    @staticmethod
    def get_all_events(page, size):
        try:
            skip = (page - 1) * size
            events_cursor = current_app.mongo.db.events.find().skip(skip).limit(size)
            events = [Event.from_dict(event).to_dict() for event in events_cursor]
            total_events = current_app.mongo.db.events.count_documents({})
            return {
                "events": events,
                "pageSize": size,
                "currentPage": page,
                "totalData": total_events
            }
        except Exception as e:
            logging.error("Error getting all events: %s", e)
            raise

    @staticmethod
    def get_user_events(user_id, page, size):
        try:
            skip = (page - 1) * size
            events_cursor = current_app.mongo.db.events.find({"ownerId": user_id}).skip(skip).limit(size)
            events = [Event.from_dict(event).to_dict() for event in events_cursor]
            total_events = current_app.mongo.db.events.count_documents({"ownerId": user_id})
            return {
                "events": events,
                "pageSize": size,
                "currentPage": page,
                "totalData": total_events
            }
        except Exception as e:
            logging.error("Error getting user events: %s", e)
            raise