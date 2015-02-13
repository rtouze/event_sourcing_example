#!/usr/bin/env python
# -*- coding: utf-8 -*-

from situation_change import *
from datetime import date
import pytest

# {{{ PersonRegistry tests
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
    assert timeline.addEventIsCalled == True


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
# }}}


# {{{ Mocks for person registry tests
class NoopEventTimeLineMock:
    def addEvent(self, eventData):
        pass

class CallCheckingEventTimeLineMock:
    def __init__(self):
        self.addEventIsCalled = False

    def addEvent(self, eventData):
        """Blah Blah Blah"""
        self.addEventIsCalled = True

class ParamCheckingEventTimeLineMock:
    def addEvent(self, eventData):
        assert eventData['type'] == 1
        assert eventData['status'] == 1
        assert eventData['personId'] == 1
        assert eventData['address']['street'] == "22 jump street"
        assert eventData['address']['city'] == "New York"
        assert eventData['name']['firstname'] == "John"
        assert eventData['name']['lastname'] == "Doe"

class ChangeStatusEventTimeLineMock:
    def __init__(self):
        self.addEventIsCalled = False

    def addEvent(self, eventData):
        self.addEventIsCalled = True
        assert eventData["type"] == 2
        assert eventData["personId"] == 1
        assert eventData["newStatus"] == Person.MARRIED
# }}}

def test_sent_events_are_retrieved():
    event_tl = EventTimeLine()
    event_tl.addEvent({
        'type': EventTimeLine.PERSON_CREATION,
        'personId': 1,
        'status': Person.SINGLE,
        'name' : { 'firstname': 'Foo', 'lastname': 'Bar' }
    })
    event_tl.addEvent({
        'type': EventTimeLine.PERSON_STATUS_CHANGE,
        'personId': 1,
        'newStatus': Person.MARRIED
    })
    event_list = list(event_tl)
    today = date.today().day
    assert len(event_list) == 2
    assert event_list[0]['type'] == EventTimeLine.PERSON_CREATION
    assert event_list[0]['_datetime'].day == today
    assert event_list[1]['type'] == EventTimeLine.PERSON_STATUS_CHANGE
    assert event_list[1]['_datetime'].day == today


# vim: fdm=marker       
