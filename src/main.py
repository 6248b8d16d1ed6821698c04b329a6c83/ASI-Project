import json
import urllib
import urllib.parse
import urllib.request
import requests
from fuzzywuzzy import process
import random
from datetime import date, datetime, timedelta
import wolframalpha
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter
c = CurrencyConverter()
import boto3
from boto3.dynamodb.conditions import Key
s3_client = boto3.client("s3")
from openai import OpenAI
import wikipedia
import html2text
import google.generativeai as genai
from oauth2client.service_account import ServiceAccountCredentials
import gspread

## Part 1: all function are define for specific action

def get_json_file(file_name):
    # import csv from s3
    bucket_name = 'asi-project-functions'
    s3_file_name = file_name
    resp = s3_client.get_object(Bucket=bucket_name,Key=s3_file_name)
    file_content = resp['Body'].read().decode("utf-8")
    json_content = json.loads(file_content)
    return json_content


def randomHello(first_name):
    # Answer with a random "Hello"
    choicesHello = ["Greetings ", "Hi ", "Welcome Back ", "Hello ", "Hey "]
    answerRandom = random.choice(choicesHello)
    answerHello = f"{answerRandom}{first_name}!"
    return answerHello 

def randomWelcome():
    # Answer with a random "You are welcome"
    choicesWelcome = ["You got it!", "Don’t mention it!", "No worries!", 
                        "Not a problem!", "My pleasure!", "It was nothing!", 
                        "I’m happy to help!", "Sure!", "Anytime!"]
    answerRandom = random.choice(choicesWelcome)
    return answerRandom 
    
def randomGood():
    # Answer with a random "I am good"
    choicesWelcome = ["I'm fine, thanks. How about you?", "Good, thanks. And you?",
                        "I'm great. And yourself?", "Good, and you?", "I'm doing well, and you?"]
    answerRandom = random.choice(choicesWelcome)
    return answerRandom 
    
def getTime():
    # Get the time
    now = datetime.now()
    currentTime = now.strftime("%Hh%M")
    textTime = f"It is now {currentTime}."
    return textTime


def getDate():
    # Get the date
    today = date.today()
    currentDate = today.strftime("%B %d, %Y")
    textDate = f"Today is {currentDate}."
    return textDate

def getAnswerWolframalpha(text):
    # App id obtained by the above steps
    app_id = get_json_file('config_credentials.json')['Wolframalpha']
    # Instance of wolf ram alpha 
    # client class
    client = wolframalpha.Client(app_id)
    # Stores the response from 
    # wolframalpha
    res = client.query(text)
    # Includes only text from the response
    answer = next(res.results).text
    return answer

def errorMessage():
    # This if error due to internet connection (useless for server)
    url = "https://fr.yahoo.com/?p=us"
    timeout = 5
    try:
        requests.get(url, timeout=timeout)
        errorMessage = ("Data is unavailable for the moment due to unknown reason.")
    except (requests.ConnectionError, requests.Timeout) as exception:
        errorMessage = ("Data is unavailable for the moment due to lack of internet connection. Send 'Help' to discover offline tools")
    return errorMessage
    

def getNews():    
    # Get top 15 news headline from BBC 
    url = 'https://www.bbc.com/news'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find('body').find_all('h2')
    unwanted = ['BBC World News TV', 'BBC World Service Radio', 'News daily newsletter', 'Mobile app', 'Get in touch', 'Video']
    newsList = "Latest Top Headlines on BBC:"
    count = 0
    for title in list(dict.fromkeys(headlines)):
        if (title.text.strip() not in unwanted) and (count < 15):
            newsList += f"\n- {title.text.strip()}."
            count += 1
    return newsList
    

def convertCurrency(amount, currency):
    '''
    Convert Currency
    Ex: convertCurrency 100 EUR/USD
    '''
    currency = currency.upper()
    currency = currency.split('/')
    currSrc = currency[0]
    currDest = currency[1]
    result = str(round(c.convert(float(amount), currSrc, currDest), 2)) + ' ' + currDest
    return result

def save_pref_data(text_input):
    # This function save preference of the user in AWS DynamoDB
    pref_adj = ["i like", "i don't like", "i do not like", "i dislike", "i love", "i hate", "i prefere", "i appreciate", "i enjoy", "i don't enjoy", "i do not enjoy"]
    sentence_low = text_input.lower()
    for x in pref_adj:
        # access memory of preferences
        dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
        table = dynamodb.Table('table_source_data')
        current_pref = table.query(KeyConditionExpression=Key('main_param').eq('memory'))
        current_pref_str = str(current_pref['Items'][0]['details_source'])
        if x in sentence_low:
            full_pref = f"{current_pref_str}, {sentence_low}"
            reponse = table.update_item(Key={"main_param": "memory"}, UpdateExpression="set details_source= :r", ExpressionAttributeValues={":r": full_pref}, ReturnValues="UPDATED_NEW",)
            return f"{current_pref_str}."
        else:
            return f"{current_pref_str}. Use only some of these information if relevant."

def get_answer_chatgpt(prompt):
    client = OpenAI(api_key=get_json_file('config_credentials.json')['chat_gpt'])
    # the message includes system parameters, memory of preference and the prompt
    message = [{"role": "system", "content": [{"type": "text","text": "My name is Constantin."}]},
                {"role": "user","content": [{"type": "text","text": prompt}]}]
    response = client.chat.completions.create(model="gpt-4o", messages=message, temperature=1, max_tokens=501)
    return response.choices[0].message.content

def gemini_prompt(text):
    genai.configure(api_key=get_json_file('config_credentials.json')['gemini'])
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(text)
    return response.text.replace('**', '').replace('*', '  - ')

def add_reminder(date, event):
    '''
    This function add an event to 'Reminder' Google Sheet.
    The command needs to be: AddEvent: Date - Event
    '''
    #Preparation Import Google Sheet
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(get_json_file('client_secret.json'), scope)
    client = gspread.authorize(credentials)
    #Import Sheet
    spreadsheet = client.open('Reminder')
    worksheet = spreadsheet.sheet1
    records_data = worksheet.get_all_records()
    # Get Last Cell Number + 1
    end_cel_num = len(records_data)+2
    # Update Last Cell
    worksheet.update(f'A{end_cel_num}:B{end_cel_num}', [[date, event]])
    # Send confirmation
    #answer = f"Thank you for your input. The event '{event}' on {date} has been added to the 'Reminder' Google sheet."
    answer = "Warning: add_reminder funtion has been disabled. Please use Reminder app on your phone."
    return answer

def execute_post_request(url, json, data):
    # Warning, this can be a huge security leak
    response = requests.post(url, json = json, data=data)
    return str(response.json())

def getAnswerWikipedia(keyword):
    try:
        # Define search
        search = 'en wikipedia org' + keyword
        url = 'https://www.google.com/search'
        # Define parameters
        headers = {'Accept' : '*/*', 'Accept-Language': 'en-US,en', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',}
        parameters = {'q': search}
        # Make the request
        content = requests.get(url, headers = headers, params = parameters).text
        soup = BeautifulSoup(content, 'html.parser')
        # Extract the first link
        search = soup.find(id = 'search')
        first_link = search.find('a')
        # Extract the proper name of the page
        name_page = first_link['href'].split("/")[-1]
        # Get text of the page
        wikipedia.set_lang("en")
        page = wikipedia.summary(name_page)
        # Extract the first paragraph
        first_paragraph = page.split("\n")[0]
        if first_paragraph != '':
            answer = first_paragraph
        else:
            answer = "Sorry, I could not find that information on Wikipedia. Try to reformulate or change search engine"
        return answer
    except:
        return "Sorry, I could not find that information on Wikipedia. Try to reformulate or change search engine"
    
def get_direction_googlemaps(origin, destination, mode):
    '''
    This function returns route and direction from google maps
    origin and destination corresponds to address or location coordinates
    mode can be: walking, bicycling, driving, transit
    '''
    api_key = get_json_file('config_credentials.json')['google_map'] 
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode={mode}&key={api_key}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)    
    answer = json.loads(response.text)
    total_distance = answer['routes'][0]['legs'][0]['distance']['text']
    duration = answer['routes'][0]['legs'][0]['duration']['text']
    start_address = answer['routes'][0]['legs'][0]['start_address']
    end_address = answer['routes'][0]['legs'][0]['end_address']
    full_text = ""
    for step in answer['routes'][0]['legs'][0]['steps']:
        next_step = html2text.html2text(step['html_instructions']).strip().replace("*", "").replace("\n\n", " * ")
        distance = step['distance']['text']
        full_text += f"\n-> {next_step} ({distance})"
    full_text_ready = f"From {start_address}\nTo {end_address}\n{duration} ({total_distance}) by {mode}\n{full_text}"
    return full_text_ready
    
def get_data_source():
    "This function check on DynamoDB what is the current default source of data"
    dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
    table = dynamodb.Table('table_source_data')
    response = table.query(KeyConditionExpression=Key('main_param').eq('name_source'))
    return response['Items'][0]['details_source']
    
def get_location():
    "This function check on DynamoDB what is the current location"
    dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
    table = dynamodb.Table('table_source_data')
    response = table.query(KeyConditionExpression=Key('main_param').eq('location'))
    return response['Items'][0]['details_source'].split(", ")[2]

def set_data_source(entry):
    if entry != "":
        entry = entry.lower()
        "This function update the default source in DynamoDB"
        choice_data_source = ["wikipedia", 'gemini', 'bard', "openai", "chatgpt", "worlframalpha", "claude"]
        result_source = process.extractOne(entry, choice_data_source)
        format_src = {'chatgpt':'ChatGPT-4o', 'gemini':'Gemini 1.5 Flash', 'bard':'Gemini 1.5 Flash', 'claude':'Claude', 'wikipedia': 'Wikipedia', 'openai': 'ChatGPT-4o', 'worlframalpha': 'WolframAlpha'}
        format_src_str = format_src[str(result_source[0])]
        if format_src_str == get_data_source():
            return f"I am already using {format_src_str} as default sources."
        else:
            if result_source[1] > 80:
                dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
                table = dynamodb.Table('table_source_data') 
                response = table.update_item(Key={"main_param": "name_source"}, UpdateExpression="set details_source= :r", ExpressionAttributeValues={":r": format_src_str}, ReturnValues="UPDATED_NEW",)
                return f"Done! I will now be using {format_src_str} as default sources."
            else:
                return "I am afraid I could not understand which source did you choose. You can either choose ChatGPT, Wikipedia or Wolframalpha"
    else:
        return "Please precise a new default sources."

def get_claude_answer(text):
    """
    This function call Claude API and return the answer.
    """
    api_key = get_json_file('config_credentials.json')['claude']
    headers = {'x-api-key': api_key,'anthropic-version': '2023-06-01','content-type': 'application/json',}
    json_data = {'model': 'claude-3-5-sonnet-20240620','max_tokens': 1024,'messages': [{'role': 'user','content': text,},],}
    response = requests.post('https://api.anthropic.com/v1/messages', headers=headers, json=json_data)
    return response.json()['content'][0]['text']

def set_location(entry):
    if entry != "":
        "This function update the location in DynamoDB"
        dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
        table = dynamodb.Table('table_source_data') 
        response = table.update_item(Key={"main_param": "location"}, UpdateExpression="set details_source= :r", ExpressionAttributeValues={":r": entry}, ReturnValues="UPDATED_NEW",)
        city = entry.split(", ")[2]
        return f"Done! I will now be using {city} as new location."
    else:
        return "Please precise a new location."

def get_weather_data(location='', hour=2):
    if location=='':
        dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
        table = dynamodb.Table('table_source_data')
        response = table.query(KeyConditionExpression=Key('main_param').eq('location'))
        location = response['Items'][0]['details_source']
    location = location.split(", ")
    api_key = get_json_file('config_credentials.json')['meteo_france']
    id_data_param = [['temperature', 'TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND', '2'],
                    ['total precipitation rate', 'TOTAL_PRECIPITATION_RATE__GROUND_OR_WATER_SURFACE', ''],
                    ['medium cloud cover', 'MEDIUM_CLOUD_COVER__GROUND_OR_WATER_SURFACE', ''],
                    ['low cloud cover', 'LOW_CLOUD_COVER__GROUND_OR_WATER_SURFACE', ''],
                    ['high cloud cover', 'HIGH_CLOUD_COVER__GROUND_OR_WATER_SURFACE', ''],
                    ['wind speed', 'WIND_SPEED__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND', '10'],
                    ['relative humidity', 'RELATIVE_HUMIDITY__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND', '2'],
                    ['atmospheric pressure', 'PRESSURE__GROUND_OR_WATER_SURFACE', '']]
    time_now = datetime.utcnow()
    time_in_2 = time_now + timedelta(hours=hour)
    if hour == 24:
        time_formated = time_in_2.strftime("%Y-%m-%dT12:00:00Z")
        time_details = "tomorrow"
    else:
        time_formated = time_in_2.strftime("%Y-%m-%dT%H:00:00Z")
        time_details = f"in {hour} hours"
    cmd_measures = f"Using the following data that you will convert to France standard, generate a short text in english presenting the weather in {location[2]} {time_details} ({time_formated}) adding a cheerful recommendation: "
    
    def get_measure_from_xml(xml_string):
        # Find the start and end of the measure value in the XML string
        start_tag = "<gml:tupleList>"
        end_tag = "</gml:tupleList>"
        # Extract the measure value by locating the tags
        start_index = xml_string.find(start_tag) + len(start_tag)
        end_index = xml_string.find(end_tag)
        # Get the measure as a substring and convert to float
        measure = xml_string[start_index:end_index].strip()
        return float(measure)

    for x in id_data_param:
        ressource = 'arome/1.0/wms/MF-NWP-HIGHRES-AROME-001-FRANCE-WMS/GetCapabilities?service=WMS&version=1.3.0&language=eng'
        url = f"https://public-api.meteofrance.fr/public/{ressource}&accept=*/*&apikey={api_key}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        #On sélectionne l'ensemble des layers contenus dans la réponse
        ensemble_des_layers = soup.find_all("layer")
        #On les parcourt jusqu'à trouver celui qui correspond à l'ID recherché
        ID = x[1]
        for layer in ensemble_des_layers:
            #print(layer.find("name").text)
            if layer.find("name").text == ID :
                break
            else:
                pass
        #On recherche les prévisions disponibles dans ce layer :
        previsions_disponibles = layer.find("dimension", {"name":"reference_time"}).text.split(",")
        #On récupére la date de la dernière prevision
        date_derniere_prevision = previsions_disponibles[-1]
        #Et on construit l'ID de la prévision correspondante 
        derniere_prevision = f"{ID}___{date_derniere_prevision}"
        derniere_prevision = derniere_prevision.replace(':','%3A')
        ressource = f"/arome/1.0/wcs/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS/GetCoverage?service=WCS&version=2.0.1&coverageid={derniere_prevision}"
        subset_time = time_formated
        subset_lat = location[0]
        subset_lon = location[1]
        if x[2] == '':
            url = f"https://public-api.meteofrance.fr/public{ressource}&subset=time({subset_time})&subset=lat({subset_lat})&subset=long({subset_lon})&format=application%2Fwmo-grib&apikey={api_key}"
        else:
            url = f"https://public-api.meteofrance.fr/public{ressource}&subset=time({subset_time})&subset=lat({subset_lat})&subset=long({subset_lon})&subset=height({x[2]})&format=application%2Fwmo-grib&apikey={api_key}"
        response = requests.get(url)
        # Example XML input (your provided document)
        xml_string = response.text
        # Get measure
        measure = get_measure_from_xml(xml_string)
        cmd_measures += f"{x[0]}: {measure}, "
    return get_answer_chatgpt(cmd_measures)


## Part 2: the algorithm choose the proper function to call 
def analyseCommand(messageInput):
    '''
    This function analyse the command in the text.
    If the analysis is not sure enough it will return an error message.
    '''  
    choices = ['hello', 'hi', 'hey', 'news', 'help', 'calculator',
               'convertcurrency', 'compute', 'howareyou', 'gemini',
               'time', 'date', 'goodmorning', 'thankyou', 'executepostrequest',
               'wikipedia', 'openai', 'chatgpt', 'wolframealpha', 
               "googlemaps", "direction", 'addreminder',
               "whatcanyoudo", "whataremaincommands", "whatareyou",
               "whatisyourname", "whocreatedyou", "whatsyourpurpose", 
               "whereareyou", "getdefaultsources", "setdefaultsources",
               "getlocation", "setlocation", "claude", "weather", "weathertomorrow"]
    resultInput = process.extractOne(messageInput, choices)
    if resultInput[1] > 70:
        commandInput = resultInput[0]
        return commandInput
    else:
        return messageInput


def defineSecondEntry(parametersEntry):
    '''
    Define the parameters for argument in function
    '''
    entrySplit = parametersEntry.split()
    if len(entrySplit) > 1:
        text = [' '.join(entrySplit[0:-1])][0]
        extraParameter = entrySplit[-1]
    else:
        text = entrySplit[0:][0]
        extraParameter = ''
    return text, extraParameter


def nameCommand(entry, secondEntry, first_name):
    '''
    Launch the requested command from commandLibrary
    '''
    
    # Level 1 commands correspond to personality (pre-recorded answers)
    lvl_1_cmd = ['help', 'whatcanyoudo', 'whataremaincommands', 'whatareyou', 'whatisyourname', 'whocreatedyou', 'whatsyourpurpose', 'whereareyou']
    if entry in lvl_1_cmd:
        return get_json_file('config_params.json')[entry]
    
    # Level 2 commands correspond to predefined actions
    if entry == 'hello' or entry == 'goodmorning' or entry == 'hi' or entry == 'hey':
        return randomHello(first_name)
    if entry == 'getdefaultsources':
        return f"The current default source is {get_data_source()}."
    if entry == 'setdefaultsources':
        try:
            return set_data_source(secondEntry)
        except:
            return errorMessage()
    if entry == 'getlocation':
        return f"The current location is {get_location()}."
    if entry == 'setlocation':
        try:
            return set_location(secondEntry)
        except:
            return errorMessage()   
    if entry == 'weather':
        try:
            return get_weather_data(location=secondEntry)
        except:
            return errorMessage()  
    if entry == 'weathertomorrow':
        try:
            return get_weather_data(location=secondEntry, hour=24)
        except:
            return errorMessage() 
    if entry == 'howareyou':
        return randomGood()
    if entry == 'time':
        return getTime()
    if entry == 'date':
        return getDate()
    if entry == 'thankyou':
        return randomWelcome()
    if entry =='addreminder':
        try:
            split_scd_entry = secondEntry.split(" * ")
            date = split_scd_entry[0]
            event = split_scd_entry[1]
            return add_reminder(date, event)
        except:
            return errorMessage() 
        
    if entry == 'convertcurrency':
        secondEntry = defineSecondEntry(secondEntry)
        try:
            return convertCurrency(secondEntry[0], secondEntry[1])
        except:
            return errorMessage()
    if entry == 'calculator' or entry == 'compute' or entry == 'wolframealpha':
        try:
            return getAnswerWolframalpha(secondEntry)
        except:
            return errorMessage()
    if entry == 'news':
        try:
            return getNews()
        except:
            return errorMessage()
    if entry == "executepostrequest":
        try:
            split_scd_entry = secondEntry.split(" * ")
            return execute_post_request(split_scd_entry[0], eval(split_scd_entry[1]), eval(split_scd_entry[2]))
        except:
            return errorMessage()
    if entry == 'wikipedia':
        try:
            return getAnswerWikipedia(secondEntry)
        except:
            return errorMessage()
    if entry == 'chatgpt' or entry == 'openai':
        try:
            return get_answer_chatgpt(secondEntry)
        except:
            return errorMessage()
    if entry == 'gemini':
        try:
            return gemini_prompt(secondEntry)
        except:
            return errorMessage()
    if entry == 'claude':
        try:
            return get_claude_answer(secondEntry)
        except:
            return errorMessage()
    if entry == 'googlemaps' or entry == 'direction':
        try: 
            split_scd_entry = secondEntry.split(" * ")
            origin = split_scd_entry[0]
            destination = split_scd_entry[1]
            mode = split_scd_entry[2].lower()
            return get_direction_googlemaps(origin, destination, mode)
        except:
            return errorMessage()  
    else:
        # Level 3 commands are free answers based on different search engines
        try:
            default_source = get_data_source()
            if default_source == "ChatGPT-4o":
                return get_answer_chatgpt(entry)
            if default_source == "Gemini 1.5 Flash":
                return gemini_prompt(entry)
            if default_source == "Wikipedia":
                return getAnswerWikipedia(entry)
            if default_source == "Claude":
                return get_claude_answer(entry)
            else:
                return getAnswerWolframalpha(entry)
        except:
            return errorMessage()

# Command to launch the full script
def mainScript(entryInput, first_name):
    #Clean the input
    entryInput = entryInput.replace("please", "")
    #Split main command and parameters
    if "$" in entryInput:
        entrySplit = entryInput.split("$ ")
        entry = entrySplit[0]
        parametersEntry = entrySplit[1]
    else:
        entry = entryInput
        parametersEntry = ''

    # Return the command
    return nameCommand(analyseCommand(entry), parametersEntry, first_name)
    
    
## Part 3: Run the whole script with the input
def lambda_handler(event, context):
    # The API support call from Telegram and POST method.
    ## POST method should contain same auth as Telegram in body as JSON string.
    try:
        print(event)
        body=json.loads(event['body'])
        
        """
        try:
            # Start with Telegram user
            print('Trying Telegram Method')
            # filter to allow only main user
            chat_id=body['message']['chat']['id']
            secret_telegram = get_json_file('config_credentials.json')['telegram']
            url = f'https://api.telegram.org/bot{secret_telegram}/sendMessage'
            allowed_user = get_json_file('config_credentials.json')['telegram_user']
            first_name = body['message']['chat']['first_name']
            
            if chat_id == allowed_user:
                # run algorithm for allowed user
                message_part=body['message'].get('text')
                data = {'url': message_part}
                message_answer = mainScript(message_part, first_name)
                payload = {'chat_id': chat_id,
                            'text': message_answer}
                r = requests.post(url,json=payload)
                return  {"statusCode": 200}
            else:
                message_answer = f"Sorry {first_name} but you do not have access to this bot. Send a message to the owner to get access."
                payload = {'chat_id': chat_id,
                            'text': message_answer}
                r = requests.post(url,json=payload)
                return  {"statusCode": 200}
        
        except:
        """
        
        # else POST request
        print('Trying POST Method')
        # filter to allow only main user
        chat_id=body['id']
        allowed_user = get_json_file('config_credentials.json')['telegram_user']
        first_name = body['first_name']
        
        if chat_id == allowed_user:
            # run algorithm for allowed user
            message_part=body['message']
            message_answer = mainScript(message_part, first_name)
            return  {"statusCode": 200, 'body': json.dumps(message_answer)}
        
        else:
            return  {"statusCode": 400, 'body': json.dumps("Something went wrong with the POST request. Make sure you enter all parameters")}
        
    except:
        return  {"statusCode": 400, 'body': json.dumps("Something went wrong.")}
