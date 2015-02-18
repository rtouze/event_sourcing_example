#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from situation_change import *

timeline = EventTimeLine()
registry = PersonRegistry(timeline)
read_registry = PersonRegistryReader()
timeline.add_subscriber(read_registry)

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
def get(person_id):
    p = read_registry.get_person_by_id(int(person_id))
    return "It's {0} {1}, he is {2}".format(
        p.name.firstname,
        p.name.lastname,
        p.status_label)


app.run(host='localhost', port=8080, reloader=True)
