#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from situation_change import *

timeline = EventTimeLine()
registry = PersonRegistry(timeline)
read_registry = PersonRegistryReader()
timeline.add_subscriber(read_registry)
timeline.add_subscriber(BasicLogger())

app = bottle.Bottle()

@app.route('/')
def index():
    return bottle.static_file('index.htm', 'static')


@app.route('/create', method='POST')
def create():
    forms = bottle.request.forms
    lastname = forms.get('lastname')
    firstname = forms.get('firstname')
    status = forms.get('status')
    person_id = registry.create(
        Person(status, Address(None, None), Name(firstname, lastname))
    )
    bottle.redirect('/{0}'.format(person_id))


@app.route('/<person_id>')
@bottle.view('person')
def get(person_id):
    p = read_registry.get_person_by_id(int(person_id))
    return {
        'p': p,
        'person_id': person_id,
        'statuses': [(Person.MARRIED, 'Married'), (Person.SINGLE, 'Single')]
    }


@app.route('/<person_id>/change_address', method='POST')
def change_address(person_id):
    forms = bottle.request.forms
    registry.move_house(int(person_id), Address(forms['new_street'], forms['new_city']))
    bottle.redirect('/{0}'.format(person_id))


@app.route('/<person_id>/change_status', method='POST')
def change_status(person_id):
    forms = bottle.request.forms
    registry.change_status(int(person_id), int(forms['new_status']))
    bottle.redirect('/{0}'.format(person_id))


bottle.debug(True)
app.run(host='localhost', port=8080, reloader=True)
