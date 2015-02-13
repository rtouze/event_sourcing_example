#!/usr/bin/env python
# -*- coding: utf-8 -*-

from situation_change import *
import pytest

@pytest.fixture
def person():
    return Person(
        status=Person.SINGLE,
        address=Address(street="22 jump street", city="New York"),
        name=Name(firstname="John", lastname="Doe")
    )


def test_a_person_id_is_generated_when_a_person_is_created(person):
    # I create a mock for my tests, because I know I'll need to access the
    # timeline in the future.
    timeline = NoopEventTimeLineMock()

    # Person registry. The only service I plan to do
    service = PersonRegistry(timeline)

    # person data object creation
    returned_id = service.create(person)
    assert returned_id != 0

def test_person_creation_event_is_stored_in_timeline(person):
    timeline = CallCheckingEventTimeLineMock()
    service = PersonRegistry(timeline)
    service.create(person)
    assert timeline.createPersonIsCalled == True

def test_person_creation_event_is_created_with_expected_set_of_argument(person):
    timeline = ParamCheckingEventTimeLineMock()
    service = PersonRegistry(timeline)
    service.create(person)

def test_person_changing_status_is_saved_in_the_timeline():
    timeline = ChangeStatusEventTimeLineMock()
    service = PersonRegistry(timeline)
    personId = 1
    newStatus = Person.MARRIED
    service.changeStatus(personId, newStatus)
    assert timeline.addEventIsCalled == True

class NoopEventTimeLineMock:

    def createPerson(self, personData):
        pass

class CallCheckingEventTimeLineMock:
    def __init__(self):
        self.createPersonIsCalled = False

    def createPerson(self, personData):
        """Blah Blah Blah"""
        self.createPersonIsCalled = True

class ParamCheckingEventTimeLineMock:
    """Blah Blah Blah"""

    def createPerson(self, personData):
        assert personData['status'] == 1
        assert personData['address']['street'] == "22 jump street"
        assert personData['address']['city'] == "New York"
        assert personData['name']['firstname'] == "John"
        assert personData['name']['lastname'] == "Doe"

class ChangeStatusEventTimeLineMock:
    def __init__(self):
        self.addEventIsCalled = False

    def addEvent(self, eventData):
        self.addEventIsCalled = True
        assert eventData["type"] == 2
        assert eventData["personId"] == 1
        assert eventData["newStatus"] == Person.MARRIED



        
        
