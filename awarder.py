"""Awarder."""
import ssl
import faust
from configs import config
from configs.badge_configuration import badges as badge_config
from configs.config import awarder_configuration
from configs.config import datastore_configuration
from events.ludus_event import LudusEvent
from ludus.datastore import Datastore
import json
import re


# Setting up Faust app
ssl_context = ssl.create_default_context(
    purpose=ssl.Purpose.SERVER_AUTH, cafile=config.kafka_configuration['cacert_file'])
app = faust.App(awarder_configuration['faust_app_name'],
                broker='kafka://' +
                config.kafka_configuration['bootstrap_server'],
                broker_credentials=ssl_context,
                store=awarder_configuration['faust_store'])

# Setting Kafka topic for stream processors
events = app.topic(config.kafka_configuration['topic'], value_type=LudusEvent)

# Initializing faust tables
event_data = app.Table(
    awarder_configuration['events_table_name'], default=None, partitions=8)
awarded_badges = app.Table(
    awarder_configuration['badges_table_name'], default=None, partitions=8)

# Initializing datastore
datastore = Datastore.get_datastore(datastore_configuration['type'])

# Initializing lookup data


def get_event_to_badge():
    """Get event to badge."""
    event_to_badges = dict()
    for badge_name in badge_config.keys():
        badge = badge_config[badge_name]
        badge['name'] = badge_name

        if badge['criteria']['type'] == 'count' or badge['criteria']['type'] == 'every_event':
            if badge['event_type'] in event_to_badges:
                badges = event_to_badges[badge['event_type']]
                badges.append(badge)
                event_to_badges[badge['event_type']] = badges
            else:
                badges = list()
                badges.append(badge)
                event_to_badges[badge['event_type']] = badges
        elif badge['criteria']['type'] == 'match':
            for matching_event in badge['criteria']['matching_events']:
                if matching_event['event_type'] in event_to_badges:
                    badges = event_to_badges[matching_event['event_type']]
                    badges.append(badge)
                    event_to_badges[matching_event['event_type']] = badges
                else:
                    badges = list()
                    badges.append(badge)
                    event_to_badges[matching_event['event_type']] = badges

    return event_to_badges


event_to_badges = get_event_to_badge()


# Processes ludus event stream
@app.agent(events)
async def aggregate_events(events):
    """Aggregate events."""
    async for event in events.group_by(LudusEvent.username):
        if event.type is None:
            event_dict = event.__dict__
            if event.username not in event_data:
                data = get_table_template()
                updated_data = update_data(data, event_dict)
                event_data[event.username] = updated_data
            else:
                data = event_data[event.username]
                updated_data = update_data(data, event_dict)
                event_data[event.username] = updated_data

            evaluate_user_data_for_badges(event_dict)


# Functions to update event data of a particular user
def update_data(data, event):
    """Function to update event data of a particular user."""
    updated_count_data = update_count(data, event)
    updated_match_data = update_match(updated_count_data, event)
    return updated_match_data


def update_count(data, event):
    """Update count."""
    count = 0
    if event['event_type'] in data['count']:
        count = data['count'][event['event_type']]
        count += 1
    else:
        count = 1

    data['count'][event['event_type']] = count
    return data


def update_match(data, event):
    """Update match."""
    if event['event_type'] not in event_to_badges:
        return data

    badges = event_to_badges[event['event_type']]

    for badge in badges:
        if badge['criteria']['type'] == 'match':
            if badge['name'] not in data['match']:
                data['match'][badge['name']] = dict()

            matching_events = badge['criteria']['matching_events']

            for matching_event in matching_events:
                if matching_event['event_type'] == event['event_type']:
                    match_value = get_match_value(
                        matching_event['field'], event)

                    if match_value in data['match'][badge['name']]:
                        state = set(data['match'][badge['name']][match_value])
                        state.add(event['event_type'])
                        data['match'][badge['name']][match_value] = state
                    else:
                        state = set()
                        state.add(event['event_type'])
                        data['match'][badge['name']][match_value] = state
    return data


def evaluate_user_data_for_badges(event):
    """Evaluate user data for badges."""
    if event_data is not None:
        for badge in event_to_badges[event['event_type']]:
            award_badge(event['username'], badge['name'], badge, event)


def award_badge(username, badge_name, badge_details, event):
    """Award badge."""
    criteria_type = badge_details['criteria']['type']

    if criteria_type == 'count':
        award_badge_for_type_count(username, badge_name, badge_details)
    elif criteria_type == 'match':
        award_badge_for_type_match(username, badge_name, badge_details, event)
    elif criteria_type == 'every_event':
        award_badge_for_type_every_event(
            username, badge_name, badge_details, event)


def is_badge_awarded(username, badge_name):
    """Check badge awarded."""
    if (username not in awarded_badges) or (awarded_badges[username] is None):
        return False
    elif badge_name in awarded_badges[username]:
        return True
    return False


def award_badge_for_type_count(username, badge_name, badge_details):
    """Award badge for type count."""
    equality = badge_name
    if is_badge_awarded(username, equality):
        return

    event_count = event_data[username]['count'][badge_details['event_type']]

    if event_count >= badge_details['criteria']['value']:
        store_badge(username, badge_name, badge_details, equality)


def award_badge_for_type_match(username, badge_name, badge_details, event):
    """Award badge for type match."""
    states = event_data[username][badge_details['criteria']
                                  ['type']][badge_name]
    field = get_matching_field(
        badge_details['criteria']['matching_events'], event)
    match_value = get_match_value(field, event)
    state = states[match_value]
    equality = badge_name + '_' + str(match_value)

    if is_badge_awarded(username, equality):
        return

    for matching_event in badge_details['criteria']['matching_events']:
        if matching_event['event_type'] not in state:
            return

    store_badge(username, badge_name, badge_details, equality)
    del event_data[username][badge_details['criteria']
                             ['type']][badge_name][match_value]


def award_badge_for_type_every_event(username, badge_name, badge_details, event):
    """Award badge for type every event."""
    equality = badge_name+' '+event['timestamp'].strftime("%s")
    if is_badge_awarded(username, equality):
        return

    store_badge(username, badge_name, badge_details, equality)


def get_matching_field(matching_events, event):
    """Get matching field."""
    for matching_event in matching_events:
        if matching_event['event_type'] == event['event_type']:
            return matching_event['field']


def get_match_value(match_field, event):
    """Get match value."""
    is_json = re.search('[.]+', match_field)

    if is_json:
        fields = match_field.split('.')
        match_value = event[fields[0]]

        for i in range(1, len(fields)):
            match_value = match_value[fields[i]]
    else:
        match_value = event[match_field]

    return str(match_value)


# Builds a skeleton Faust table template, should be changed when new Criteria is added
def get_table_template():
    """Build a skeleton Faust table template, should be changed when new Criteria is added."""
    table_template = {
        'count': dict(),
        'match': dict()
    }
    return table_template


# Creates a badge and stores it in Faust table so that are not reawareded to a User
def store_badge(username, badge_name, badge_details, equality):
    """Create a badge and stores it in Faust table so that are not reawareded to a User."""
    new_badge = {
        'type': 'badge',
        'username': username,
        'badge': badge_name,
        'description': badge_details['description'],
        'criteria': badge_details['criteria'],
        'equality': equality
    }

    if (new_badge['username'] not in awarded_badges) or awarded_badges[new_badge['username']] is None:
        awarded_badges[new_badge['username']] = set()

    awarded_badges_to_current_user = set(awarded_badges[new_badge['username']])
    awarded_badges_to_current_user.add(new_badge['equality'])
    awarded_badges[new_badge['username']] = awarded_badges_to_current_user

    new_badge_json = json.dumps(new_badge)
    datastore.insert(new_badge_json.encode('utf-8'))


if __name__ == "__main__":
    """Main method."""
    app.main()
