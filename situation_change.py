#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


# {{{ Services
class PersonRegistry:
    """Provide services to deal with people"""

    def __init__(self, timeline):
        """Initialize timeline event"""
        self.timeline = timeline
        self._currentId = 0

    def create(self, person):
        """Create a person in the system"""
        self._currentId += 1
        self.timeline.add_event({
            'type': EventTimeLine.PERSON_CREATION,
            'personId': self._currentId,
            'status': person.status,
            'address': person.address.to_dict(),
            'name': person.name.to_dict()
        })
        return self._currentId

    def changeStatus(self, personId, newStatus):
        self.timeline.add_event({
            'type': EventTimeLine.PERSON_STATUS_CHANGE,
            'personId': personId,
            'newStatus': newStatus
        })

    def get_person_by_id(self, demanded_id):
        returned_person = None
        print("Timeline:" + str(list(self.timeline)))
        person_events = (
            p for p in self.timeline 
            if p['personId'] == demanded_id
        )
        for event in person_events:
            print('Event:' + str(event))
            if event['type'] == EventTimeLine.PERSON_CREATION:
                returned_person = Person(
                    event['status'],
                    None,
                    Name(
                        event['name']['firstname'],
                        event['name']['lastname']
                        )
                )
            if event['type'] == EventTimeLine.PERSON_STATUS_CHANGE:
                returned_person.status = event['newStatus']
        return returned_person
        
# }}}


# {{{ Domain model
class Person:

    SINGLE = 1
    MARRIED = 2
    LABELS = {
        1: 'single',
        2: 'married'
    }

    def __init__(self, status, address, name):
        self.status = int(status)
        self.address = address
        self.name = name

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


class EventTimeLine:
    """Basically, the list of all events in the system. Allows to add an event.
    The object itself is iterable if you want to browse the created events."""

    PERSON_CREATION = 1
    PERSON_STATUS_CHANGE = 2

    def __init__(self):
        """Initialize the inner event list"""
        self.event_list = []

    def add_event(self, event_data):
        """Add an event in the event list."""
        event_data['_datetime'] = datetime.datetime.today()
        self.event_list.append(event_data)

    def __iter__(self):
        for e in self.event_list:
            yield e
# vim: fdm=marker
