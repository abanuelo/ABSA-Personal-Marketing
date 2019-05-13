import os
import re
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

'''This script will be used to separate all the traning data and testing
data for personalized marketing'''
#List containing all keywords for auto service repair
keywords = ['ac', 'airbag', 'air bag', 'air condition', 'air conditioning', 'conditioning',
            'compress', 'compressor', 'evaporator', 'heating', 'blower motor', 'a/c', 
            'evaporat', 'freon', 'heat', 'air filter', 'airfilter', 'air fltr', 'air filters',
            'air cleaner', 'alternator', 'abs', 'ball joint', 'ball joints', 'brake', 'brakes', 
            'brk', 'rotor', 'pad', 'caliper', 'brake pad', 'brake pads', 'rotors', 'pads', 
            'calipers', 'brake system fluid', 'brake fluid', 'brake system flush', 'brake flush',
            'battery', 'belt', 'belts', 'blt', 'body', 'fender', 'molding', 'bumper', 'trim', 
            'door', 'trunk', 'hood', 'mirror', 'filler', 'grille', 'quarter panel', 'rear quarter',
            'paint', 'decal', 'convertible', 'water leak', 'mould', 'windshield', 'hail', 'refinish',
            'applique', 'baffle', 'bar', 'bed', 'blower', 'box', 'brace', 'cargo', 'carpet',
            'carrier', 'child', 'clock', 'compartment', 'cushion', 'deflector', 'dent', 'emblem', 
            'fascia', 'flaps', 'gate', 'glass', 'grill', 'guard', 'guide', 'handle', 'hinge',
            'insulat', 'label', 'latch', 'leg', 'lever', 'lid', 'lite', 'lock', 'luggage', 'nob', 
            'panel', 'rail', 'reflector', 'retainer', 'roof', 'running board', 'seat', 'shade', 
            'speaker', 'spindle', 'spoiler', 'step', 'strap', 'striker', 'strip', 'top', 'window', 
            'clear coat', 'door latch', 'batt', 'battery', 'starter', 'bulb', 'bulbs', 'head light', 
            'boot', 'boots', 'cv', 'cabin air filter', 'cabin air', 'hepa', 'cabin filter', 'hvac filter',
            'pollen', 'clutch', 'check engine light', 'coils', 'coil', 'cool', 'cooling', 'radiat', 
            'radiator', 'thermostat', 'coolant', 'bear', 'bearing', 'axle', 'axles', 'differential', 
            'diff', 'awd', 'elect', 'electric', 'electrical', 'tensioner', 'intake gasket', 'water pump', 
            'waterpump', 'control valve', 'vent', 'head gasket', 'oil pan', 'o ring', 'o rings', 
            'oring', 'orings', 'head gaskets', 'engine', 'exhaust', 'exh', 'muff', 'muffler', 'manifold', 
            'catalytic', 'cat convert', 'cat converter', 'egr', 'fuel', 'induction', 'hose', 'ingnition', 
            'intermediate mile', 'intermediate mileage', 'inter mile', 'inter mileage', 'knob', 'major service', 
            'service major', 'major maintenance service', 'maintenance service', 'maintenance minder',
            'year maintenance service', 'year service', 'year svc', 'intermediate service', 'psmp', 
            'maint service', 'service light on', 'service light', 'mile service', 'mile maintenance', 
            'mile main', 'mile', 'mile light service', 'major mile', 'major mileage', 'recall', 'minor service', 
            'service minor', 'minor svc', 'minor mile', 'minor mileage', 'multi-point', 'multi-point inspection', 
            'multipoint inspection', 'multi point inspection', 'multi-point visual inspection', 
            'multipoint visual inspection', 'mpi', 'visual inspection', 'inspection', 'point inspection', 
            'new tire', 'new tires', 'tire', 'tires', 'four tire', 'four tires', 'tire', 'tires', 
            'two tire', 'two tires', 'tire', 'one tire', 'rear tire', 'rear wheel', 'rear tires', 'front tire',
            'front wheel', 'front tires', 'side tire', 'side tires', '1 new tire', 'one new tire', 'replace tire', 
            'replace tires', 'replacing tire', 'replacing tires', 'replacement tire', 'replacement tires', 'tire bald',
            'tires bald', 'bald tire', 'bald tires', 'balding tire', 'balding tires', 'tire replacement', 'tire', 
            'tires', 'nitro', 'nitrogen', 'oil filter', 'oil & filter', 'lof', 'l.o.f.', 'l.o.f', 'lube service', 
            'oil and filter', 'express service', 'quick lube', 'quick service', 'oil w filter', 'oil change', 
            'lube oil', 'oil & filter', 'express oil', 'oil service', 'engine oil', 'mobil one', 'oil + filter', 'oil change', 
            'oil leak', 'oil leaking', 'fluid leak', 'fluid leaking', 'oil leaks', 'fluid leaks', 'fluid levels', 
            'leakage', 'leak', 'repair', 'repairs', 'recall', 'service', 'serv', 'svc', 'ser', 'safety inspection', 
            'safety inspect', 'safety inspec', 'sensor', 'sensors', 'spark', 'sparkplug', 'sparkplugs', 'spark plug', 
            'spark plugs', 'state inspection', 'state inspect', 'state inspec', 'st inspection', 'st inspect', 'st inspec', 
            'emission inspection', 'emission inspect', 'emission inspec', 'obd', 'steer', 'steering', 'pinon', 'pinion', 
            'power-steer', 'power-steering', 'control arm', 'controlarm', 'powersteering', 'ps', 'pdi', 'arm', 'susp',
            'suspension', 'strut', 'struts', 'shock', 'shocks', 'bushing', 'bushings', 'upper control arm', 'sway bar',
            'throttle body', 'throttle', 'tie rod', 'tie rods', 'tire rot', 'tire rotation', 'rotate tire', 'rotate tires', 
            'rotating tire', 'rotating tires', 'rotated tire', 'rotated tires', 'tpms sensor', 'trans', 'transmission', 
            'transfer', 'tranny', 'trany', 'cvt flush', 'cvt flushes', 'pdk service', 'pdk', 'transmission system fluid',
            'transmission fluid', 'transmission system flush', 'transmission flush', 'pdk flush', 'pdk fluid', 'tune', 
            'tuneup', 'align', 'alignment', 'wheel alignment', 'mounted', 'balance', 'mount and balance tires', 
            'mount and balance tire', 'balance tires', 'balance tire', 'mount and balance', 'wiper', 'wipers', 'wiper blade', 
            'wiper blades', 'wiperblade', 'wiperblades', 'wiper insert', 'wiper inserts']
#Remove any duplicates from the list
keywords = list(set(keywords))

#Will output textfile 
file = open('data_to_prep.txt', 'a')

#Import CSV File and Insert Comments into List
df = pd.read_excel('Declined_Final.xlsx', sheet_name='Sheet1')
listOfComments = df['comment']

for x in listOfComments:
    #Convert data to lowercase
    x = x.lower()
    #Remove any quantitative elements, and extraneous characters from sentence (vehicle id, psi pressure, ***, --, etc)
    regex = re.compile('[^A-Za-z |]+')
    x = regex.sub('', x)
    #Split sentences at the '|' delimitter
    sentences = x.split('|')
    #Iterate through sentences to see what keywords exist in sentence in order to label their sentiment
    for s in sentences:
        if len(s) > 0:
            file.write('-'*40 + '\n')
            file.write(s + '\n')
            file.write('-'*40 + '\n')
            for w in keywords:
                if w in s: 
                    file.write(w + '\n')
                

    