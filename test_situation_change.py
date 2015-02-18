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
    assert timeline.add_event_is_called == True


def test_person_creation_event_is_created_with_expected_set_of_argument(person):
    timeline = ParamCheckingEventTimeLineMock()
    service = PersonRegistry(timeline)
    service.create(person)


def test_person_changing_status_is_saved_in_the_timeline():
    timeline = ChangeStatusEventTimeLineMock()
    service = PersonRegistry(timeline)
    personId = 1
    newStatus = Person.MARRIED
    service.change_status(personId, newStatus)
    assert timeline.add_event_is_called == True

def test_person_can_be_retrieved_by_id_with_actual_status():
    # EventTimeLine object is iterable therfore I can
    # replace it with a simple list to test read access.
    tl = EventTimeLine()
    read_registry = PersonRegistryReader()
    tl.add_subscriber(read_registry)
    
    service = PersonRegistry(tl)
    person_id_1 = service.create(
        Person(
            Person.SINGLE,
            Address('Somewhere', 'Thailand'),
            Name('John', 'Rambo')
        )
    )
    person_id_2 = service.create(
        Person(
            Person.SINGLE,
            Address('Somewhere else', 'Zanzibar'),
            Name('Ada', 'Wong')
        )
    )
    service.change_status(person_id_1, Person.MARRIED)

    person = read_registry.get_person_by_id(person_id_1)
    assert person.name.lastname == 'Rambo'
    assert person.status == Person.MARRIED
    assert person.status_label == "married"

    person2 = read_registry.get_person_by_id(person_id_2)
    assert person2.status_label == "single"

def test_that_the_system_is_affected_by_address_change():
    tl = EventTimeLine()
    read_registry = PersonRegistryReader()
    tl.add_subscriber(read_registry)
    
    service = PersonRegistry(tl)
    person_id_1 = service.create(
        Person(
            Person.SINGLE,
            Address('Somewhere', 'Thailand'),
            Name('John', 'Rambo')
        )
    )
    service.move_house(person_id_1, Address('Some beach', 'Phuket'))
    person = read_registry.get_person_by_id(person_id_1)
    assert person.address.street == 'Some beach'
    assert person.address.city == 'Phuket'
# }}}


# {{{ Mocks for person registry tests
class NoopEventTimeLineMock:
    def add_event(self, event_data):
        pass

    def add_subscriber(self, object):
        pass

class CallCheckingEventTimeLineMock:
    def __init__(self):
        self.add_event_is_called = False

    def add_event(self, event_data):
        self.add_event_is_called = True

    def add_subscriber(self, object):
        pass
        

class ParamCheckingEventTimeLineMock:
    def add_event(self, event_data):
        assert event_data['type'] == 1
        assert event_data['status'] == 1
        assert event_data['personId'] == 1
        assert event_data['address']['street'] == "22 jump street"
        assert event_data['address']['city'] == "New York"
        assert event_data['name']['firstname'] == "John"
        assert event_data['name']['lastname'] == "Doe"

    def add_subscriber(self, object):
        pass

class ChangeStatusEventTimeLineMock:
    def __init__(self):
        self.add_event_is_called = False

    def add_event(self, event_data):
        self.add_event_is_called = True
        assert event_data["type"] == 2
        assert event_data["personId"] == 1
        assert event_data["newStatus"] == Person.MARRIED

    def add_subscriber(self, object):
        pass
# }}}

def test_sent_events_are_retrieved():
    event_tl = EventTimeLine()
    event_tl.add_event({
        'type': EventTimeLine.PERSON_CREATION,
        'personId': 1,
        'status': Person.SINGLE,
        'name' : { 'firstname': 'Foo', 'lastname': 'Bar' }
    })
    event_tl.add_event({
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
