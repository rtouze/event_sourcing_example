#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        self.timeline.addEvent({
            'type': EventTimeLine.PERSON_CREATION,
            'status': person.status,
            'address': person.address.to_dict(),
            'name': person.name.to_dict()
        })
        return self._currentId;

    def changeStatus(self, personId, newStatus):
        self.timeline.addEvent({
            'type': EventTimeLine.PERSON_STATUS_CHANGE,
            'personId': personId,
            'newStatus': newStatus
        })
# }}}

# {{{ Domain model
class Person:

    SINGLE = 1
    MARRIED = 2

    def __init__(self, status, address, name):
        self.status = status
        self.address = address
        self.name = name

class Name:
    """Blah Blah Blah"""

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
        return { 'street': self.street, 'city': self.city }
# }}}


class EventTimeLine:
    """Blah Blah Blah"""

    PERSON_CREATION = 1
    PERSON_STATUS_CHANGE = 2

    def __init__(self):
        """Blah Blah Blah"""
        
# vim: fdm=marker       
