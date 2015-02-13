#!/usr/bin/env python
# -*- coding: utf-8 -*-

from situation_change import *
import pytest

@pytest.fixture
def person():
    return Person(Person.SINGLE, Adress(street="22 jump street", city="New York"))


def test_a_person_id_is_generated_when_a_person_is_created(person):
    # I create a mock for my tests, because I know I'll need to access the
    # timeline in the future.
    timeline = NoopEventTimeLineMock()

    # Person registry. The only service I plan to do
    service = PersonRegistry(timeline)

    # person data object creation
    #person = Person(Person.SINGLE, Adress(street="22 jump street", city="New York"))
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


        
        