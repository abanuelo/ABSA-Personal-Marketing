import os
import numpy as np
import re
import infer_example

'''
Rudimentary User-Feedback Feature to get evaluation. 
Author: Armando Banuelos
Date: 5/15/19
'''

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
            'multipoint visual inspection', 'mpi', 'multipoint', 'visual inspection', 'inspection', 'point inspection', 
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

#Dictionary that contains information about the category of service based on keyword
serviceToKeyword = {'Air Bag Service':['airbag'], 
                    'Air Condition Service':['aircondition', 'airconditioning', 'conditioning', 'compress', 'compressor', 'evaporator','heating','blowermotor','ac','evaporat','freon','heat'],
                    'Air Filter Service':['airfilter','airfltr','airfilters','aircleaner'], 
                    'Alternator':['alternator'],
                    'ABS Service':['abs'],
                    'Ball Joint Service':['balljoint','balljoints'],
                    'Brake Service':['brake','brakes','brk','rotor','pad','caliper','brakepad','brakepads','rotors','pads','calipers'],
                    'Brake Fluid Service':['brakesystemfluid','brakefluid','brakesystemflush','brakeflush'],
                    'Battery Service':['battery'],
                    'Belt Service':['belt','belts','blt'],
                    'Body Repair':['body','fender','molding','bumper','trim','door','trunk','hood','mirror','filler','grille','quarterpanel','rearquarter','paint','decal','convertible','waterleak','mould','windshield','hail','refinish','applique','baffle','bar','bed','blower','box','brace','cargo','carpet','carrier','child','clock','compartment','cushion','deflector','dent','emblem','fascia','flaps','gate', 'glass', 'grill', 'guard', 'guide', 'handle', 'hinge', 'insulat', 'label', 'latch', 'leg', 'lever', 'lid', 'lite', 'lock', 'luggage', 'nob', 'panel', 'rail', 'reflector', 'retainer', 'roof', 'runningboard', 'seat', 'shade', 'speaker', 'spindle', 'spoiler', 'step', 'strap', 'striker', 'strip', 'top','window','clearcoat', 'doorlatch'],
                    'Battery Service':['batt', 'battery', 'starter'],
                    'Bulb Replacement': ['bulb', 'bulbs',  'headlight'],
                    'C/V Boot Service': ['boot', 'boots', 'cv'],
                    'Cabin Air Filter Service': ['cabinairfilter', 'cabinair', 'hepa', 'cabinfilter', 'hvacfilter', 'pollen'],
                    'Clutch Service': ['clutch'],
                    'Check Engine Light': ['checkenginelight'],
                    'Coils' : ['coils', 'coil'],
                    'Cooling System Service': ['cool', 'cooling', 'radiat', 'radiator', 'thermostat', 'coolant'],
                    'Drive Train Service': ['bear', 'bearing', 'axle', 'axles', 'differential', 'diff', 'awd'],
                    'Electrical Service': ['elect', 'electric', 'electrical'],
                    'Engine Service': ['tensioner', 'intakegasket', 'waterpump', 'controlvalve', 'vent', 'headgasket', 'oilpan', 'oring', 'orings', 'headgaskets', 'engine'],
                    'Exhaust System Service': ['exhaust', 'exh', 'muff', 'muffler', 'manifold', 'catalytic', 'catconvert','catconverter', 'egr'],
                    'Fuel System Service': ['fuel', 'induction'],
                    'Hose Service': ['hose'],
                    'Ignition Service': ['ingnition'],
                    'Intermediate Mileage Service': ['intermediatemile', 'intermediatemileage', 'intermile', 'intermileage'],
                    'Knob Service': ['knob'],
                    'Major Maintenance Service': ['majorservice', 'servicemajor', 'majormaintenanceservice'],
                    'Maintenance Service' :['maintenanceservice', 'maintenanceminder','yearmaintenanceservice', 'yearservice', 'yearsvc', 'intermediateservice', 'psmp', 'maintservice', 'servicelighton', 'servicelight'],
                    'Mile Service' : ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice'],
                    'Major Mileage Service': ['majormile', 'majormileage'],
                    'Manufacturer Recall': ['recall'],
                    'Minor Maintenance Service': ['minorservice', 'serviceminor', 'minorsvc'],
                    'Minor Mileage Service': ['minormile', 'minormileage'],
                    'Multi-Point Inspection': ['multipoint', 'multipointinspection','multipointvisualinspection', 'mpi', 'visualinspection', 'inspection', 'pointinspection'],
                    'New Tire(s)': ['newtire', 'newtires', 'fourtire', 'fourtires', 'twotire', 'twotires','onetire', 'reartire', 'rearwheel', 'reartires', 'fronttire', 'frontwheel','fronttires','sidetire', 'sidetires','onenewtire','replacetire', 'replacetires', 'replacingtire', 'replacingtires', 'replacementtire','replacementtires','tirebald', 'tiresbald', 'baldtire', 'baldtires', 'baldingtire', 'baldingtires','tirereplacement','tire', 'tires'],
                    'Nitrogen Fill Tires': ['nitro', 'nitrogen'],
                    'Oil & Filter Change': ['oilfilter', 'oilandfilter', 'lof', 'lubeservice','expressservice','quicklube', 'quickservice', 'oilwfilter', 'oilchange', 'lubeoil','expressoil','oilservice', 'engineoil', 'mobilone', 'oilfilter', 'oilchange'],
                    'Oil/Fluid Leak Repair': ['oilleak', 'oilleaking', 'fluidleak', 'fluidleaking', 'oilleaks', 'fluidleaks', 'fluidlevels', 'leakage', 'leak'],
                    'Repairs' : ['repair', 'repairs'],
                    'Service' : ['service', 'serv', 'svc' , 'ser'],
                    'Safety Inspection': ['safetyinspection', 'safetyinspect', 'safetyinspec'],
                    'Sensor Service': ['sensor', 'sensors'],
                    'Spark Plugs': ['spark', 'sparkplug', 'sparkplugs', 'sparkplug', 'sparkplugs'],
                    'State Emissions Inspection': ['stateinspection', 'stateinspect', 'stateinspec', 'stinspection', 'stinspect','stinspec','emissioninspection', 'emissioninspect', 'emissioninspec', 'obd'],
                    'Steering Service': ['steer', 'steering', 'pinon', 'pinion', 'powersteer', 'powersteering', 'controlarm','controlarm', 'powersteering', 'ps', 'pdi', 'arm'],
                    'Suspension Service': ['susp', 'suspension', 'strut', 'struts', 'shock', 'shocks', 'bushing', 'bushings','uppercontrolarm', 'swaybar'],
                    'Throttle Body Service': ['throttlebody', 'throttle'],
                    'Tie Rod Service': ['tierod', 'tierods'],
                    'Tire Rotation': ['tirerot', 'tirerotation', 'rotatetire', 'rotatetires', 'rotatingtire', 'rotatingtires', 'rotatedtire', 'rotatedtires'],
                    'TPMS Service': ['tpmssensor'],
                    'Transmission Service': ['trans', 'transmission', 'transfer', 'tranny', 'trany', 'cvtflush', 'cvtflushes', 'pdkservice', 'pdk'],
                    'Transmission Flush Service': ['transmissionsystemfluid', 'transmissionfluid','transmissionsystemflush', 'transmissionflush', 'pdkflush', 'pdkfluid'],
                    'Tune Up': ['tune', 'tuneup'],
                    'Wheel Alignment Service': ['align', 'alignment', 'wheelalignment'],
                    'Wheel Balance': ['mounted', 'balance', 'mountandbalancetires', 'mountandbalancetires', 'mountandbalancetires', 'mountandbalancetire', 'balancetires', 'mountandbalance'],
                    'Wiper Blade Service': ['wiper', 'wipers', 'wiperblade', 'wiperblades', 'wiperblade', 'wiperblades', 'wiperinsert','wiperinserts']}

def cleanInput(user_input):
    #Convert to lowercase for that data
    user_input = user_input.lower()
    #Remove any quantitative elements, and extraneous characters from sentence (vehicle id, psi pressure, ***, --, etc)
    regex = re.compile('[^A-Za-z |]+')
    user_input = regex.sub('', user_input)
    #Split sentences at the ' ' delimitter
    sentences = user_input.split(' ')
    #Delete excess spaces contained with the sentence
    while('' in sentences):
        sentences.remove('')
    return sentences

def extractSentenceAndKeywords(cleaned_input):
    sentence = ""
    k = []
    true_sentence = ' '.join(cleaned_input)
    if len(cleaned_input) > 0:
        for w in keywords:
            if w in true_sentence:
                #check if > 1 word keywords to single word
                w_list = w.split(' ')
                if (len(w_list) > 1):
                    new_w = ''.join(w_list)
                    k.append(new_w)
                    true_sentence = true_sentence.replace(w, new_w)
                else:
                    k.append(w)
        sentence = true_sentence
    return sentence, k

def findCategory(keyword):
    for key, val in serviceToKeyword.items():
        if keyword in val:
            return key

def main():
    print("Introducing LSTM Deep Learning Aspect Based Sentiment Analysis")
    print("-"*75)
    print("Please insert an automobile report and we will try our best to find")
    print("what was performed, recommended, or declined in your servicing history!")
    print('\n')
    print("As an example consider this:")
    print("\'Inspected hood to check if coolant fine. Consider replacing coolant\'")
    print('\n')
    while(True):
        user_input = input(">> ")
        cleaned_input = cleanInput(user_input)
        sentence, k = extractSentenceAndKeywords(cleaned_input)
        list_of_outputs = []
        for key in k: 
            category = findCategory(key)
            sentiment = infer_example.main(sentence, key, '')
            if sentiment[0] == 1:
                output = "Completed service on: " + category
                if output not in list_of_outputs:
                    list_of_outputs.append(output)
                    print(output)
            elif sentiment[0] == -1:
                output = "Declined service on: " + category
                if output not in list_of_outputs:
                    list_of_outputs.append(output)
                    print(output)
            elif sentiment[0] == 0:
                output = "Recommended service on: " + category
                if output not in list_of_outputs:
                    list_of_outputs.append(output)
                    print(output)



if __name__ == "__main__":
    main()