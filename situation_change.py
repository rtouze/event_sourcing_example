#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PersonRegistry:
    """Provide services to deal with people"""

    def __init__(self, timeline):
        """Initialize timeline event"""
        self.timeline = timeline
        self._currentId = 0 

    def create(self, person):
        """Create a person in the system"""
        self._currentId += 1
        self.timeline.createPerson({
            'status': person.status,
            'address': person.address.to_dict(),
            'name': person.name.to_dict()
        })
        return self._currentId;

class Person:

    SINGLE = 1
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
