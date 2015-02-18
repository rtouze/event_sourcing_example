#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging


# {{{ Services
class PersonRegistry:
    """Provide services to deal with people"""

    def __init__(self, timeline):
        """Initialize timeline event"""
        self._timeline = timeline
        self._current_id = 0
        self._registry = {}

    def _generate_person_id(self):
        # Generate a system identifier. In a real application, it should be
        # externalized or ensure that a unique id is generated.
        self._current_id += 1
        return self._current_id

    def create(self, person):
        """Create a person in the system"""
        current_id = self._generate_person_id()
        self._timeline.add_event({
            'type': EventTimeLine.PERSON_CREATION,
            'personId': current_id,
            'status': person.status,
            'address': person.address.to_dict(),
            'name': person.name.to_dict()
        })
        return current_id

    def change_status(self, personId, newStatus):
        """Ask to change the status of a person"""
        self._timeline.add_event({
            'type': EventTimeLine.PERSON_STATUS_CHANGE,
            'personId': personId,
            'newStatus': newStatus
        })

    def move_house(self, person_id, new_address):
        """Change the address of a person"""
        self._timeline.add_event({
            'type': EventTimeLine.PERSON_MOVE,
            'personId': person_id,
            'newAddress': {
                'street': new_address.street,
                'city': new_address.city
            }
        })
# }}}

# {{{ PersonRegistryReader
class PersonRegistryReader:
    """PersonRegistry aimed at read access"""

    def __init__(self):
        """Initialize the read registry"""
        self._registry = {}

    def notify(self, data):
        """Get notified that something happened in the system. It should be
        called by an event emmitter only to update internal data
        representation."""

        if 'personId' in data.keys():
            person_id = data['personId']
            if data['type'] == EventTimeLine.PERSON_CREATION:
                self._registry[person_id] = {
                    'name': data['name'],
                    'address': data['address'],
                    'status': data['status'],
                    'version': 1
                }

            if data['type'] == EventTimeLine.PERSON_STATUS_CHANGE:
                p = self._registry[person_id]
                p['status'] = data['newStatus']
                p['version'] += 1

            if data['type'] == EventTimeLine.PERSON_MOVE:
                p = self._registry[person_id]
                p['address'] = data['newAddress']
                p['version'] += 1

    def get_person_by_id(self, demanded_id):
        """Retrieve a person from it's identifier in the system."""
        stored_person = self._registry[demanded_id]
        returned_person = Person(
            stored_person['status'],
            Address(
                stored_person['address']['street'],
                stored_person['address']['city']
            ),
            Name(
                stored_person['name']['firstname'],
                stored_person['name']['lastname']
                ),
            stored_person['version']
        )
        return returned_person

    def __hash__(self):
        return id(self)
# }}}

# {{{ BasicLogger
class BasicLogger:
    """Basic logger that can be attached to the event source"""

    def __init__(self):
        """Blah Blah Blah"""
        self._logger = logging.getLogger('EventSent')
        self._logger.setLevel(level=logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(level=logging.INFO)
        formatter = logging.Formatter(
            '%(name)s - %(levelname)s - %(asctime)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

    def notify(self, data):
        self._logger.info(str(data))
# }}}

# {{{ Domain model
class Person:

    SINGLE = 1
    MARRIED = 2
    LABELS = {
        1: 'single',
        2: 'married'
    }

    def __init__(self, status, address, name, version=1):
        self.status = int(status)
        self.address = address
        self.name = name
        self.version = version

    @property
    def status_label(self):
        return self.LABELS[self.status]


class Name:
    def __init__(self, firstname, lastname):
        """Blah Blah Blah"""
        self.firstname, self.lastname = firstname, lastname

    def to_dict(self):
        return {'firstname': self.firstname, 'lastname': self.lastname}


class Address:
    def __init__(self, street, city):
        self.street = street
        self.city = city

    def to_dict(self):
        return {'street': self.street, 'city': self.city}
# }}}

# {{{ EventTimeLine
class EventTimeLine:
    """Basically, the list of all events in the system. Allows to add an event.
    The object itself is iterable if you want to browse the created events."""

    PERSON_CREATION = 1
    PERSON_STATUS_CHANGE = 2
    PERSON_MOVE = 3

    def __init__(self):
        """Initialize the inner event list"""
        self.event_list = []
        self._subscribers = set()

    def add_event(self, event_data):
        """Add an event in the event list."""
        event_data['_datetime'] = datetime.datetime.today()
        self.event_list.append(event_data)
        self._notify_all(event_data)

    def add_subscriber(self, object):
        """Allow to an object to subscribe to the event TL. Method *notify* on
        this object will be called at any event pushed in the event
        timeline."""
        self._subscribers.add(object)

    def _notify_all(self, event_data):
        """Notify all the subscribers of a change, sending them event_data"""
        for subs in self._subscribers:
            subs.notify(event_data)

    def __iter__(self):
        for e in self.event_list:
            yield e
# }}}
# vim: fdm=marker
