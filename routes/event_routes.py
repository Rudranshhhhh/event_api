from flask import Blueprint, request, jsonify
import requests
from facade.event_facade import EventFacade
from decorators import token_required, permission_required

event_bp = Blueprint('event_bp', __name__)

# Static variables
ROLE_SUPERADMIN = 'superAdmin'
ROLE_ADMIN = 'admin'
ROLE_USER = 'user'
ERROR_EVENT_NOT_FOUND = {'error': 'Event not found'}
ERROR_PERMISSION_DENIED = {'error': 'Permission denied'}

@event_bp.route('/event/create', methods=['POST'])
@token_required
def create_event(current_user, current_user_role):
    data = request.get_json()
    event = EventFacade.create_event(
        ownerId=current_user,
        type=data['type'],
        title=data['title'],
        description=data['description'],
        date=data['date'],
        from_time=data['from'],
        to_time=data['to'],
        location=data['location'],
        group=data.get('group', ['default']),
        organizer=data['organizer']
    )
    return jsonify(event)

@event_bp.route('/event/<event_id>', methods=['GET'])
@token_required
def get_event(current_user, current_user_role, event_id):
    event = EventFacade.get_event(event_id)
    if event:
        if event['is_public'] or event['ownerId'] == current_user or current_user_role in [ROLE_ADMIN, ROLE_SUPERADMIN]:
            return jsonify(event)
        else:
            return jsonify(ERROR_PERMISSION_DENIED), 403
    return jsonify(ERROR_EVENT_NOT_FOUND), 404

@event_bp.route('/event/<event_id>', methods=['PUT'])
@token_required
@permission_required(ROLE_USER)
def update_event(current_user, current_user_role, event_id):
    data = request.get_json()
    
    event = EventFacade.get_event(event_id)
    if not event:
        return jsonify(ERROR_EVENT_NOT_FOUND), 404

    if current_user_role not in [ROLE_ADMIN, ROLE_SUPERADMIN] and event['ownerId'] != current_user:
        return jsonify(ERROR_PERMISSION_DENIED), 403

    success = EventFacade.update_event(
        event_id,
        ownerId=data.get('ownerId'),
        type=data.get('type'),
        title=data.get('title'),
        description=data.get('description'),
        date=data.get('date'),
        from_time=data.get('from'),
        to_time=data.get('to'),
        location=data.get('location'),
        group=data.get('group'),
        organizer=data.get('organizer')
    )
    if success:
        return jsonify({'message': 'Event updated'})
    return jsonify(ERROR_EVENT_NOT_FOUND), 404

@event_bp.route('/event/<event_id>', methods=['DELETE'])
@token_required
@permission_required(ROLE_USER)
def delete_event(current_user, current_user_role, event_id):

    event = EventFacade.get_event(event_id)
    if not event:
        return jsonify(ERROR_EVENT_NOT_FOUND), 404

    if current_user_role not in [ROLE_ADMIN, ROLE_SUPERADMIN] and event['ownerId'] != current_user:
        return jsonify(ERROR_PERMISSION_DENIED), 403
    
    success = EventFacade.delete_event(event_id)
    if success:
        return jsonify({'message': 'Event deleted'})
    return jsonify(ERROR_EVENT_NOT_FOUND), 404

@event_bp.route('/event/list', methods=['GET'])
@token_required
@permission_required(ROLE_USER)
def list_events(current_user, current_user_role):
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    
    if current_user_role == ROLE_SUPERADMIN:
        events_data = EventFacade.get_all_events(page, size)
    else:
        events_data = EventFacade.get_user_events(current_user, page, size)
    
    return jsonify(events_data)

@event_bp.route('/event/share/<event_id>', methods=['POST'])
@token_required
def share_event(current_user, current_user_role, event_id):
    data = request.get_json()
    event = EventFacade.get_event(event_id)
    if not event:
        return jsonify(ERROR_EVENT_NOT_FOUND), 404

    share_methods = data.get('methods', [])
    recipients = data.get('recipients', [])

    if 'sms' in share_methods:
        send_sms(event, recipients)

    if 'email' in share_methods:
        send_email(event, recipients)

    if 'notification' in share_methods:
        send_notification(event, recipients)

    return jsonify({'message': 'Event shared successfully'})

def send_sms(event, recipients):
    # Implement SMS sending logic here
    for recipient in recipients:
        # Example API call to send SMS
        response = requests.post('https://sms-api.example.com/send', json={
            'to': recipient,
            'message': f"Event: {event['title']} on {event['date']} at {event['location']}"
        })
        if response.status_code != 200:
            print(f"Failed to send SMS to {recipient}")

def send_email(event, recipients):
    # Implement email sending logic here
    for recipient in recipients:
        # Example API call to send email
        response = requests.post('https://email-api.example.com/send', json={
            'to': recipient,
            'subject': f"Invitation to {event['title']}",
            'body': f"Event: {event['title']}\nDate: {event['date']}\nLocation: {event['location']}\nDescription: {event['description']}"
        })
        if response.status_code != 200:
            print(f"Failed to send email to {recipient}")

def send_notification(event, recipients):
    # Implement notification sending logic here
    for recipient in recipients:
        # Example API call to send notification
        response = requests.post('https://notification-api.example.com/send', json={
            'to': recipient,
            'title': f"Invitation to {event['title']}",
            'body': f"Event: {event['title']}\nDate: {event['date']}\nLocation: {event['location']}\nDescription: {event['description']}"
        })
        if response.status_code != 200:
            print(f"Failed to send notification to {recipient}")