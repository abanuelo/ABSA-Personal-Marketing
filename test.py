import os
import re
import math
import pandas as pd
import sys
sys.path.insert(0, './atae-lstm-cabasc/')
import infer_abs
import infer_airbag
import infer_airconditioner
import infer_balljoint
import infer_cabinairfilter
import infer_oil

#Will include all the servicing categories:
serviceToKeyword = {'Air Bag Service':['airbag'], 
                    'Air Condition Service':['aircondition', 'airconditioning', 'conditioning', 'compress', 'compressor', 'evaporator','heating','blowermotor','ac','evaporat','freon','heat'],
                    'Air Conditioning Service':['aircondition', 'airconditioning', 'conditioning', 'compress', 'compressor', 'evaporator','heating','blowermotor','ac','evaporat','freon','heat'],
                    'Air Filter Service':['airfilter','airfltr','airfilters','aircleaner'], 
                    'Alternator':['alternator'],
                    'ABS Service':['abs'],
                    'Ball Joint Service':['balljoint','balljoints'],
                    'Brake Service':['brake','brakes','brk','rotor','pad','caliper','brakepad','brakepads','rotors','pads','calipers'],
                    'Brak Service':['brake','brakes','brk','rotor','pad','caliper','brakepad','brakepads','rotors','pads','calipers'],
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
                    'Intermediate Maintenance Service' :['maintenanceservice', 'maintenanceminder','yearmaintenanceservice', 'yearservice', 'yearsvc', 'intermediateservice', 'psmp', 'maintservice', 'servicelighton', 'servicelight'],
                    '2 Year(s) Maintenance Service' : ['maintenanceservice', 'maintenanceminder','yearmaintenanceservice', 'yearservice', 'yearsvc', 'intermediateservice', 'psmp', 'maintservice', 'servicelighton', 'servicelight','majorservice', 'servicemajor', 'majormaintenanceservice'],
                    '4 Year(s) Maintenance Service' : ['maintenanceservice', 'maintenanceminder','yearmaintenanceservice', 'yearservice', 'yearsvc', 'intermediateservice', 'psmp', 'maintservice', 'servicelighton', 'servicelight','majorservice', 'servicemajor', 'majormaintenanceservice'],
                    'Mile Service' : ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice'],
                    'Major Mileage Service': ['majormile', 'majormileage'],
                    '10000 Miles Maintenance Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    '30,000 Mile Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    '20,000 Mile Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    '100,000 Mile Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    '40,000 Mile Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    '30000 Miles Maintenance Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    '20000 Miles Maintenance Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    '40000 Miles Maintenance Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    '60000 Miles Maintenance Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    '100000 Miles Maintenance Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    '120000 Miles Maintenance Service': ['mileservice', 'milemaintenance',  'milemain', 'mile' , 'milelightservice', 'majormile', 'majormileage'],
                    'Manufacturer Recall': ['recall'],
                    'Minor Maintenance Service': ['minorservice', 'serviceminor', 'minorsvc'],
                    'Minor Mileage Service': ['minormile', 'minormileage'],
                    'Multi-Point Inspection': ['multipoint', 'multipointinspection','multipointvisualinspection', 'mpi', 'visualinspection', 'inspection', 'pointinspection'],
                    'New Tire(s)': ['newtire', 'newtires', 'fourtire', 'fourtires', 'twotire', 'twotires','onetire', 'reartire', 'rearwheel', 'reartires', 'fronttire', 'frontwheel','fronttires','sidetire', 'sidetires','onenewtire','replacetire', 'replacetires', 'replacingtire', 'replacingtires', 'replacementtire','replacementtires','tirebald', 'tiresbald', 'baldtire', 'baldtires', 'baldingtire', 'baldingtires','tirereplacement','tire', 'tires'],
                    'New  Tire(s)': ['newtire', 'newtires', 'fourtire', 'fourtires', 'twotire', 'twotires','onetire', 'reartire', 'rearwheel', 'reartires', 'fronttire', 'frontwheel','fronttires','sidetire', 'sidetires','onenewtire','replacetire', 'replacetires', 'replacingtire', 'replacingtires', 'replacementtire','replacementtires','tirebald', 'tiresbald', 'baldtire', 'baldtires', 'baldingtire', 'baldingtires','tirereplacement','tire', 'tires'],
                    'Nitrogen Fill Tires': ['nitro', 'nitrogen'],
                    'Oil & Filter Change': ['oilfilter', 'oilandfilter', 'lof', 'lubeservice','expressservice','quicklube', 'quickservice', 'oilwfilter', 'oilchange', 'lubeoil','expressoil','oilservice', 'engineoil', 'mobilone', 'oilfilter', 'oilchange'],
                    'Oil/Fluid Leak Repair': ['oilleak', 'oilleaking', 'fluidleak', 'fluidleaking', 'oilleaks', 'fluidleaks', 'fluidlevels', 'leakage', 'leak'],
                    'Oil/Fluid Repair': ['oilleak', 'oilleaking', 'fluidleak', 'fluidleaking', 'oilleaks', 'fluidleaks', 'fluidlevels', 'leakage', 'leak'],
                    'Repairs' : ['repair', 'repairs'],
                    'Service' : ['service', 'serv', 'svc' , 'ser'],
                    'Annual Service': ['service', 'serv', 'svc' , 'ser'],
                    'Safety Inspection': ['safetyinspection', 'safetyinspect', 'safetyinspec'],
                    'Sensor Service': ['sensor', 'sensors'],
                    'Spark Plugs': ['spark', 'sparkplug', 'sparkplugs', 'sparkplug', 'sparkplugs'],
                    'State Emissions Inspection': ['stateinspection', 'stateinspect', 'stateinspec', 'stinspection', 'stinspect','stinspec','emissioninspection', 'emissioninspect', 'emissioninspec', 'obd'],
                    'State Emission Inspection': ['stateinspection', 'stateinspect', 'stateinspec', 'stinspection', 'stinspect','stinspec','emissioninspection', 'emissioninspect', 'emissioninspec', 'obd'],
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
                    'Wheel Alignment': ['align', 'alignment', 'wheelalignment'],
                    'Wheel Balance': ['mounted', 'balance', 'mountandbalancetires', 'mountandbalancetires', 'mountandbalancetires', 'mountandbalancetire', 'balancetires', 'mountandbalance'],
                    'Wiper Blade Service': [ 'wiper', 'wipers', 'wiperblade', 'wiperblades', 'wiperblade', 'wiperblades', 'wiperinsert','wiperinserts']}


#Will read through text file in order to extract keywords
def readFile(txt_file):
    f_val = []
    #Get only the second line:
    line_count = 1
    f = open(txt_file, 'r')
    for line in f:
        if (line_count == 4):
            line_count = 1
        elif (line_count == 2):
            f_val.append(line.strip('\n'))
        line_count += 1
    f_val = list(set(f_val))
    return f_val

#Collects all keywords from specified files
def collectKeywords(keywordCollection):
    #Start with File 1
    f1_key = "abs"
    f1_val = readFile("./atae-lstm-cabasc/abs.txt")
    keywordCollection[f1_key] = f1_val
    #File 2
    f2_key = "airbag"
    f2_val = readFile("./atae-lstm-cabasc/airbag.txt")
    keywordCollection[f2_key] = f2_val
    #File 3
    f3_key = "airconditioner"
    f3_val = readFile("./atae-lstm-cabasc/airconditioner.txt")
    keywordCollection[f3_key] = f3_val
    #File 4
    f4_key = "balljoint"
    f4_val = readFile("./atae-lstm-cabasc/balljoint.txt")
    keywordCollection[f4_key] = f4_val
    #File 5
    f5_key = "cabinairfilter"
    f5_val = readFile("./atae-lstm-cabasc/cabinairfilter.txt")
    keywordCollection[f5_key] = f5_val
    #File 6
    f6_key = "oil"
    f6_val = readFile("./atae-lstm-cabasc/oil.txt")
    keywordCollection[f6_key] = f6_val

#Cleans eval data (removes numbers, periods, etc)
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
    final = []
    for s in sentences:
        if '|' in s:
            s = s.replace('|', '')
        final.append(s)
    return final

#Six models: ATAE-LSTM for each sentence and keyword specified in Samples
def evalModels(model_name, sentence, key):
    sentiment = 0
    if model_name == "abs":
        sentiment = infer_abs.main(sentence, key, './atae-lstm-cabasc/')
    elif model_name == "airbag":
        sentiment = infer_airbag.main(sentence, key, './atae-lstm-cabasc/')
    elif model_name == "airconditioner":
        sentiment = infer_airconditioner.main(sentence, key, './atae-lstm-cabasc/')
    elif model_name == "balljoint":
        sentiment = infer_balljoint.main(sentence, key, './atae-lstm-cabasc/')
    elif model_name == "cabinairfilter":
        sentiment = infer_cabinairfilter.main(sentence, key, './atae-lstm-cabasc/')
    elif model_name == "oil":
        sentiment = infer_oil.main(sentence, key, './atae-lstm-cabasc/')
    return sentiment

def evaluateFromFile(keywordCollection):
    #Read In Eval Data
    df = pd.read_excel('./data/Samples.xlsx')
    comments = df['Comment']
    decline_categories = df['Declines']

    #Keeps track of current accuracy for the model
    total = 0
    curr_eval = 0

    #Keep track of specific tasks to see which one is doing better
    abs_accuracy = 0
    abs_total = 0
    airbag_accuracy = 0
    airbag_total = 0
    airconditioner_accuracy = 0
    airconditioner_total = 0
    balljoint_accuracy = 0
    balljoint_total = 0
    cabinairfilter_accuracy = 0
    cabinairfilter_total = 0
    oil_accuracy = 0
    oil_total = 0
    
    for i in range(len(comments)):
        print("Current Example Under Analysis: " + str(i+1) + " out of " + str(len(comments)))

        serviceTypes = str(decline_categories[i]).split(", ")
        #Extract all keywords associated with that service
        list_of_keywords = []
        for s in serviceTypes:
            if s in serviceToKeyword:
                keywords = serviceToKeyword[s]
                list_of_keywords += keywords

        curr_sentence = str(comments[i])
        clean = ' '.join(cleanInput(curr_sentence))
        if clean != "nan":
            #Iterate through dictionary to see if those words exist:
            for key, val in keywordCollection.items():
                for keyword in val:
                    if keyword in clean:
                        new_keyword = ''.join(keyword.split(' '))
                        if new_keyword in list_of_keywords:
                            total += 1
                            result = evalModels(key, clean, keyword)
                            if result[0] == -1:
                                curr_eval += 1

                            #Checking track of which models do best fine-grained
                            if key == "abs":
                                abs_total += 1
                                if result[0] == -1:
                                    abs_accuracy += 1
                            elif key == "airbag":
                                airbag_total += 1
                                if result[0] == -1:
                                    airbag_accuracy += 1
                            elif key == "airconditioner":
                                airconditioner_total += 1
                                if result[0] == -1:
                                    airconditioner_accuracy += 1
                            elif key == "balljoint":
                                balljoint_total += 1
                                if result[0] == -1:
                                    balljoint_accuracy += 1
                            elif key == "cabinairfilter":
                                cabinairfilter_total += 1
                                if result[0] == -1:
                                    cabinairfilter_accuracy += 1
                            elif key == "oil":
                                oil_total += 1
                                if result[0] == -1 or result[0] == 0:
                                    oil_accuracy += 1
                                else:
                                    print(curr_sentence)

    #Print statements to learn more about the model being presented
    print('\n'*5)
    if(total > 0):
        print("Current accuracy of the model is: ", float(curr_eval/total))
    if (abs_total > 0):
        print("Current abs accuracy of the model is: ", float(abs_accuracy/abs_total))     
        print("Total Examples Presented: ", abs_total)
        print("Total Examples Predicted Correctly: ", abs_accuracy)
    else:
        print("Currently no ABS Category Examples!")
    if (airconditioner_total > 0):
        print("Current airconditioner of the model is: ", float(airconditioner_accuracy/airconditioner_total))
        print("Total Examples Presented: ", airconditioner_total)
        print("Total Examples Predicted Correctly: ", airconditioner_accuracy)
    else:
        print("Current no Air Conditioning Examples!")
    if (cabinairfilter_total > 0):
        print("Current cabin air filter of the model is: ", float(cabinairfilter_accuracy/cabinairfilter_total))
        print("Total Examples Presented: ", cabinairfilter_total)
        print("Total Examples Predicted Correctly: ", cabinairfilter_accuracy)
    else: 
        print("Current no Cabin Air Filter Examples!")
    if (airbag_total > 0):
        print("Current airbag accuracy of the model is: ", float(airbag_accuracy/airbag_total))
        print("Total Examples Presented: ", airbag_total)
        print("Total Examples Predicted Correctly: ", airbag_accuracy)
    else:
        print("Currently no Air Bag Examples!")
    if (balljoint_total > 0):
        print("Current balljoint accuracy of the model is: ", float(balljoint_accuracy/balljoint_total))
        print("Total Examples Presented: ", balljoint_total)
        print("Total Examples Predicted Correctly: ", balljoint_accuracy)
    else:
        print("Currently no Balljoint Examples!")
    if (oil_total > 0):
        print("Current oil accuracy of the model is: ", float(oil_accuracy/oil_total))
        print("Total Examples Presented: ", oil_total)
        print("Total Examples Predicted Correctly: ", oil_accuracy)
    else:
        print("Currently no Oil examples!")

def evaluateFromCommandLine(keywordCollection):
    print("Introducing LSTM Deep Learning Aspect Based Sentiment Analysis With Fine Grained Categories")
    print("-"*75)
    print("Please insert an automobile report and we will try our best to find")
    print("what was performed, recommended, or declined in your servicing history!")
    print('\n')
    print("As an example consider this:")
    print("\'Inspected hood to check if coolant fine. Consider replacing coolant\'")
    print('\n')
    print("Current keywords that are under analysis: ", keywordCollection)
    print('\n')

    while(True):
        user_input = input(">> ")
        cleaned_input = ' '.join(cleanInput(user_input))
        for key, val in keywordCollection.items():
            for keyword in val:
                if keyword in cleaned_input:
                    result = evalModels(key, cleaned_input, keyword)
                    if result[0] == 1:
                        print("Performed category: ", key)
                    elif result[0] == -1:
                        print("Declined category: ", key)
                    elif result[0] == 0:
                        print("Recommended category: ", key)
                    else:
                        print("Neutral category: ", key)
                        

if __name__ == "__main__":
    keywordCollection = {}
    collectKeywords(keywordCollection)

    if sys.argv[1] == "manual_test":
        evaluateFromCommandLine(keywordCollection)
    else:
        evaluateFromFile(keywordCollection)
    
    