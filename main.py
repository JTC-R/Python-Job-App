import requests
from bs4 import BeautifulSoup
import pandas
import re
import datetime
import sys
import getpass

# Grabs list of potential websites to search
def make_website_list():
    possible_website = ['monster', 'indeed', 'getting.hired', 'flex.jobs', 'snag.a.job', 'glass.door']
    return (possible_website)

# Used for later functions for easy input-checking
def make_yes_list():
    possible_yes = ['Yes', 'yes', 'Y', 'y']
    return (possible_yes)

# used for later functions for easy input-checking
def make_no_list():
    possible_no = ['No', 'no', 'N', 'n']
    return (possible_no)

# Ensures that the answers are appropriate for website choice
def inappropriate_answer(answer, website):
    if (answer == 'answer_one'):
        print(f'Please answer with Yes or No or type \'Cancel\' to exit the program. ')
        answer = input(f'Do you want to search all of the website?\nWebsites included are: {make_website_list()}: ')
    elif (answer == 'answer_two'):
        print('Please answer with a Yes or No or type \'Cancel\' to exit the program. ')
        answer = input(f'Do you want to search {website}?: ')
    return (answer)

# Gathers, via user input, which websites to check
def get_websites():
    chosen_website = []
    possible_websites = make_website_list()
    possible_yes = make_yes_list()
    possible_no = make_no_list()
    answer_one = input(f'Do you want to search all of the websites?\n Websites included are: {make_website_list()}: ')
    while answer_one not in possible_yes and answer_one not in possible_no and answer_one != 'Cancel':
        answer_one = inappropriate_answer("answer_one", website=None)
    if (answer_one in possible_yes):
        return (possible_websites)
    elif (answer_one in possible_no):
        for website in possible_websites:
            answer_two = input(f'Do you want to search {website}? (Y/N): ')
            while answer_two not in possible_yes and answer_two not in possible_no and answer_two != 'Cancel':
                answer_two = inappropriate_answer("answer_two", website)
            if (answer_two in possible_yes):
                chosen_website.append(website)
            elif (answer_two == 'Cancel'):
                print("Exiting")
                exit()
        return (chosen_website)
    elif (answer_one == 'Cancel'):
        print("Exiting")
        exit()

# Prints list of chosen websites
def print_website_list(websites):
    print(f'The websites chosen are: {websites}')

# Gathers via user input if the user wants to search for specific jobs
def get_profession():
    possible_yes = make_yes_list()
    possible_no = make_no_list()
    answer = input("Do you want to search a specific job type? (Yes/No): ")
    while (answer not in possible_yes and answer not in possible_no):
        print("Please answer with Yes or No ")
        answer = input("Do you want to search a specific job type? (Yes/No): ")
    if (answer in possible_yes):
        return (True)
    else:
        return (False)

# Gathers via user input which jobs to search for
def which_profession():
    answer = input("Which type of job do you want to look for?: ")
    while (re.search(r'\d', answer)):
        print("Please re-input the type of job ")
        answer = input("Which type of job do you want to look for?: ")
    return (answer)

# Gathers via user input if the user wants to search additional job key-words
def multiple_professions():
    possible_yes = make_yes_list()
    answer = input("Do you want to search multiple jobs? (Yes/No): ")
    if (answer in possible_yes):
        return (True)
    else:
        return (False)

# Gathers via user input and while loop the other job key-words the user is interested in
def multiple_professions_additional():
    possible_yes = make_yes_list()
    possible_no = make_no_list()
    answer = input("Do you want to add an additional job? (Yes/No): ")
    while (answer not in possible_yes and answer not in possible_no and answer != 'Skip'):
        print("Please answer with Yes or No or type 'Skip' if you wish to skip. ")
        answer = input("Do you want to add an additional job? (Yes/No/Skip): ")
    if (answer in possible_yes):
        return (True)
    else:
        return (False)

# Removes any redundant jobs chosen by the user
def multiple_professions_redun_removal(input):
    return (list(set(input)))

# Prints for the user the list of jobs chosen
def print_job_list(jobs):
    print(f'The jobs being searched for are: {jobs}')

# Gathers via user input the city to be searched in
def get_location_city():
    amount = 0
    possible_yes = make_yes_list()
    possible_no = make_no_list()
    answer = input(f'Do you want to search for jobs in Philadelphia? (Yes/No): ')
    verified_answer = False
    while answer not in possible_yes and answer not in possible_no:
        print(f'Please answer with Yes or No. ')
        answer = input(f'Do you want to search for jobs in Philadelphia? (Yes/No): ')
    if (answer in possible_yes):
        return ("Philadelphia")
    else:
        while verified_answer == False:
            answer = input(f'In which city do you want to search for jobs?: ')
            verified_answer_input = input(f'Verifying, you want to search for a job in {answer}? (Yes/No) ')
            while verified_answer_input not in possible_yes and verified_answer_input not in possible_no:
                print(f'Please answer with either \'Yes\' or \'No\'. ')
                verified_answer_input = input(f'Verifying, you want to search for a job in {answer}? (Yes/No) ')
                amount += 1
                if (amount == 3):
                    print(f'Unable to understand. Defaulting location to Philadelphia, PA. ')
                    return ("Philadelphia")
            if (verified_answer_input in possible_yes):
                verified_answer = True
        return (answer)

# Gathers via user input which state to search in
def get_location_state(answer):
    answer = input(f'What state is {answer} in? (Please answer with 2 letter abbreviation.): ')
    input_amount = len(answer)
    while input_amount != 2:
        print(f'Please only use the two letter abbreviation for the state. ')
        answer = input(f'What state is {answer} in? (Please answer with 2 letter abbreviation.): ')
        input_amount = len(answer)
    return (answer.upper())

# Snag.a.job(?) requires ZIP code
def get_location_zip(city, state):
    answer = input(f'What is the zip code for this {city}, {state}?: ')
    return (answer)

# Formats the city, state, and zip code into format for later use
def get_location_main():
    city = get_location_city()
    state = get_location_state(city)
    zip = get_location_zip(city, state)
    location = [city, state, zip]
    print(f'Searching in {location[0]}, {location[1]} for jobs. ')
    return (location)

# Gathers via user input how many jobs are to be searched per website
def get_search_amount():
    possible_amount = list(range(1, 51))
    answer = input(
        f'How many jobs would you like to search for (per job type and website). (Type \'Explain\' for help.): ')
    while answer not in possible_amount:
        if (answer == 'Explain'):
            print(
                'If you search for a job type on a website, a certain number of responses will be generated.\nIf you want 10, for instance, then '
                'you will receive 10 results per job type searched for every website. ')
            answer = input(
                f'How many jobs would you like to search for (per job type and website). (Type \'Explain\' for help.): ')
        try:
            answer = int(answer)
            if (answer > 50):
                print(f'Please limit number of searches from 1 to 50. ')
                answer = input(
                    f'How many jobs would you like to search for (per job type and website). (Type \'Explain\' for help.): ')
        except ValueError:
            print(f'Please input only a number between 1 and 50')
            answer = input(
                f'How many jobs would you like to search for (per job type and website). (Type \'Explain\' for help.): ')
    return (answer)

def create_monster(job, location, new, amount):
    base_url = "http://www.monster.com"
    if (location[0] == "Philadelphia"):
        location = f'{location[0]}__2C-PA'
    else:
        city = location[0]
        city = re.sub(r'\s', '-', city)
        state = location[1]
        location = f'{city}__2C-{state}'
    if (job == "None"):
        full_url = f'{base_url}/jobs/search/?where={location}'
    else:
        job = re.sub(r'\s', '-', job)
        full_url = f'{base_url}/jobs/search/?q={job}&where={location}'
    if (new == False):
        amount += 1
        page_amount = f'&stpage=1&page={amount}'
        full_url = f'{base_url}/jobs/search/?q={job}&where={location}{page_amount}'
    return (full_url)

def create_indeed_url(job, location, new, amount):
    base_url = "http://www.indeed.com"
    city = location[0]
    city = re.sub(r'\s', '+', city)
    state = location[1]
    location = f'{city}%2C+{state}'
    if (job == "None"):
        full_url = f'{base_url}/jobs?l={location}&radius=5'
    else:
        job = re.sub(r'\s', '+', job)
        full_url = f'{base_url}/jobs?q={job}&l={location}&radius=5'
    if (new == False):
        amount += 1
        amount = (amount * 5) + 5
        full_url = f'{full_url}&start={amount}'
    return (full_url)

def create_zip_url(job, location, new, amount):
    base_url = "http://www.ziprecruiter.com"
    city = location[0]
    state = location[1]
    city = re.sub(r'\s', '+', city)
    location = f'{city}%2C+{state}'
    if (job == 'None'):
        full_url = f'{base_url}/candidate/search?search=&location={location}'
    else:
        job = re.sub(r'\s', '+', job)
        full_url = f'{base_url}/candidate/search?radius=25&search={job}&location={location}'
    if (new == False):
        amount += 1
        full_url = f'{full_url}&page={amount}'
    return (full_url)

def create_gettinghired_url(job, location, new, amount):
    base_url = "http://www.gettinghired.com/jobs/"
    city = location[0]
    city = re.sub(r'\s', '-', city)
    state = location[1]
    if (job == "None"):
        full_url = f'{base_url}{city}/?kw={state}'
    else:
        job = re.sub(r'\s', '-', job)
        full_url = f'{base_url}{city}/?kw={job}+{state}'
    if (new == False):
        amount += 1
        amount = (amount * 20) - 20
        full_url = f'{full_url}&ix={amount}'
    return (full_url)

def create_flexjobs_url(job, location, new, amount):
    base_url = "http://www.flexjobs.com"
    city = location[0]
    city = re.sub(r'\s', '+', city)
    state = location[1]
    location = f'{city}%2C+{state}'
    if (job == "None"):
        full_url = f'{base_url}/search?search=&search=&location={location}'
    else:
        job = re.sub(r'\s', '+', job)
        full_url = f'{base_url}/search?search={job}&location={location}'
    if (new == False):
        amount += 1
        full_url = f'{full_url}&page={amount}'
    return (full_url)

def create_snagajob_url(job, location):
    base_url = "http://www.snagajob.com/"
    location = location[2]
    if (job == "None"):
        full_url = f'{base_url}search?w={location}&radius=5'
    else:
        job = re.sub(r'\s', '+', job)
        full_url = f'{base_url}search?q={job}&w={location}&radius=5'
    return (full_url)

####
# Below is the process to find the appropriate URL when searching Glassdoor.com
# First the program is directed to the page that lists the states. It then gathers the URL directing it to the list of cities in that state
# From there various manipulations occur to produce the required URL
def create_state_dictionary():
    state_list_improper = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
                           'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
                           'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
                           'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
                           'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
                           'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE',
                           'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
                           'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
                           'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
                           'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
                           'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
                           'Wisconsin': 'WI', 'Wyoming': 'WY'}
    state_list = {v: k for k, v in state_list_improper.items()}
    return (state_list)


def call_glassdoor_url(url, header):
    page = requests.get(url, headers=header)
    if (page.status_code != 200):
        print("Unable to obtain page. ")
    else:
        return (page)

def get_content(page):
    if (page != "None"):
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            return (soup)
        except AttributeError:
            return (False)

def get_state_url_link(soup, state):
    state_url = soup.find('li', string=state).find('a')['href']
    return (state_url)

def get_state_url(state, url, header):
    page = call_glassdoor_url(url, header)
    soup = get_content(page)
    state_url_incomplete = get_state_url_link(soup, state)
    state_url = f'https://www.glassdoor.com{state_url_incomplete}'
    return (state_url)

def find_city_page(state_url, city, header):
    page = call_glassdoor_url(state_url, header)
    soup = get_content(page)
    page_number = 1
    found_city = False
    while found_city is False:
        city_section = soup.find('a', string=city)
        if (city_section != None):
            found_city = True
        else:
            page_number += 1
            if (page_number == 2):
                state_url = re.search(r'.+(?=.htm)', state_url).group(0) + "_P" + str(page_number) + ".htm"
            elif (page_number < 11):
                state_url = re.search(r'.+(?=_P\d.htm)', state_url).group(0) + "_P" + str(page_number) + ".htm"
            elif (page_number >= 11):
                state_url = re.search(r'.+(?=_P\d{2}.htm)', state_url).group(0) + "_P" + str(page_number) + ".htm"
            page = call_glassdoor_url(state_url, header)
            soup = get_content(page)
    return (city_section)

def get_city_url(section):
    city_url_raw = section['href']
    city_url = f'https://www.glassdoor.com{city_url_raw}'
    return (city_url)

def clean_city_url(city_url):
    city_code = re.search(r'(?<=IC)\d.+(?=.htm)', city_url).group(0)
    return (city_code)

def get_odd_code(url, header):
    page = requests.get(url, headers=header)
    soup = get_content(page)
    odd_code = soup.find('meta', property='og:url')['content']
    return (odd_code)

def get_k_value(url, header, location):
    url_base = url
    page_base = requests.get(url_base, headers=header)
    soup_base = BeautifulSoup(page_base.content, 'html.parser')
    next_element_raw_ = soup_base.find(string=f'Top Jobs in {location[0]}, {location[1]}').next_element
    next_element_raw = next_element_raw_.find('a')
    next_element = next_element_raw['href']
    k_value = re.search(r'.{7}(?=.htm)', next_element).group(0)
    return (k_value)

def find_proper_k_value(url, header, job):
    incomplete_url_front = re.search(r'.+(?=\d{2})', url).group(0)
    incomplete_url_back = '.htm?radius=5'
    for i in range(1, 100):
        if (i in range(1, 10)):
            i_url = f'{incomplete_url_front}0{i}{incomplete_url_back}'
        else:
            i_url = f'{incomplete_url_front}{i}{incomplete_url_back}'
        page = requests.get(i_url, headers=header)
        soup = BeautifulSoup(page.content, 'html.parser')
        response_website = soup.find('meta', property='og:url')['content']
        if (job[1:len(job)] in response_website):
            response_website = f'{response_website}?radius=5'
            return (response_website)
        else:
            page = None
            soup = None
            response_website = None
            abbreviated_url = None
    print(f'Unable to find a {job} job. ')
    return (False)

def create_glassdoor_url(job, location, new, amount):
    state_list = create_state_dictionary()
    state = state_list.get(location[1])
    city = location[0]
    ## need city modification if two names
    radius = "?radius=5"
    header = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    base_url = "https://www.glassdoor.com/sitedirectory/city-jobs.htm"
    state_url = get_state_url(state, base_url, header)
    city_section_page = find_city_page(state_url, city, header)
    city_url = get_city_url(city_section_page)
    url = city_url + radius
    if (job == "None"):
        if (new == True):
            return (url)  # This works
        else:
            amount += 1
            city_url_raw = re.search(r'.+(?=.htm)', city_url).group(0)
            city_url = f'{city_url_raw}_IP{amount}.htm'
            return (city_url)  # this works
    else:
        job = re.sub('\s', '-', job)
        k_value = get_k_value(url, header, location)
        front_url = re.search(r'.+(?=-jobs)', url, re.IGNORECASE).group(0)
        back_url = re.search(rf'(?<={city}-).+(?=.htm)', url, re.IGNORECASE).group(0)
        if (new == True):
            partial_url = f'{front_url}-{job}-{back_url}_{k_value}.htm'
            full_url = find_proper_k_value(partial_url, header, job)
            if (full_url != False):
                return (full_url)
            else:
                return (None)
        else:
            amount += 1
            partial_url = f'{front_url}-{job}-{back_url}_{k_value}.htm'
            full_url_partial = find_proper_k_value(partial_url, header, job)
            if (full_url_partial != False):
                full_url = f"{re.search(r'.+(?=.htm)', full_url_partial).group(0)}_IP{amount}.htm?radius=5"
                return (full_url)
            else:
                return (None)

### End glass.door url creation
# This aggregates the URL creations
def create_url(website, job, location, new, amount):
    if (website == 'monster'):
        url = create_monster(job, location, new, amount)
    elif (website == 'indeed'):
        url = create_indeed_url(job, location, new, amount)
    elif (website == 'zip'):
        url = create_zip_url(job, location, new, amount)
    elif (website == 'getting.hired'):
        url = create_gettinghired_url(job, location, new, amount)
    elif (website == "flex.jobs"):
        url = create_flexjobs_url(job, location, new, amount)
    elif (website == "snag.a.job"):
        url = create_snagajob_url(job, location)
    elif (website == 'glass.door'):
        url = create_glassdoor_url(job, location, new, amount)
    return (url)

# Glassdoor is a long process; this warns user.
def glass_door_warning():
    print(f'Warning! : Searching Glassdoor.com takes time. Please be patient.')

# Once the url has been generated, the URL is called with the appropriate headers
def call_url(website, full_url, job):
    if (website == 'zip'):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'sec-ch-ua': 'Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87',
            # 'Referer': 'https://www.ziprecruiter.com/candidate/search?search=&location=Philadelphia%2C+PA',
            'sec-ch-ua-mobile': '?0'}
        page = requests.get(full_url, headers=headers)
    elif (website == 'indeed'):
        headers = {
            'User-Agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 87.0 .4280 .88 Safari / 537.36',
            'sec-ch -ua': '"Google Chrome"; v = "87", " Not;A Brand"; v = "99", "Chromium"; v = "87"'}
        page = requests.get(full_url, headers=headers)
    else:
        header = {
            'User-Agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 87.0 .4280 .88 Safari / 537.36', }
        page = requests.get(full_url, headers=header)
    if (page.status_code == 200):
        return (page)
    else:
        print(f"Unable to obtain website {website} for job {job}. ")
        return ("404")

# If access is granted/bypassed then the contents of the page are parsed
def get_content(page):
    if (page != "None"):
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            return (soup)
        except AttributeError:
            return (False)

# This aggregates the required html/css code to find the results container
def get_results_container(website, soup):
    if (website == "monster"):
        results = soup.find(id='ResultsContainer')
    if (website == "indeed"):
        results = soup.find(id='resultsCol')
    if (website == "getting.hired"):
        results = soup.find(id='listing')
    if (website == "flex.jobs"):
        results = soup.find(id='joblistarea')
    if (website == "snag.a.job"):
        results = soup.find('div', class_="results")
    if (website == 'glass.door'):
        results = soup.find('div', id='JobResults')
    return (results)

# Call funciton to get the job_list
def get_job_list_handler(container, parent, child, website):
    try:
        if (website == 'snag.a.job'):
            job_elements = container.find_all(parent)
        else:
            job_elements = container.find_all(parent, class_=child)
    except AttributeError:
        print(f'No job container on {website}.')
        job_elements = False
    return (job_elements)

# Aggregate job_list caller
def get_job_list(website, results_container):
    if (website == "monster"):
        job_elements = get_job_list_handler(results_container, 'section', 'card-content', 'monster')
    elif (website == "indeed"):
        job_elements = get_job_list_handler(results_container, 'div', 'jobsearch-SerpJobCard', 'indeed')
    elif (website == "getting.hired"):
        job_elements = get_job_list_handler(results_container, 'li', 'c-lister__item', 'getting.hired')
    elif (website == "flex.jobs"):
        job_elements = get_job_list_handler(results_container, 'li', 'list-group-item job', 'flex.jobs')
    elif (website == "snag.a.job"):
        job_elements = get_job_list_handler(container=results_container, parent='job-overview', website='snag.a.job',
                                            child=None)
    elif (website == 'glass.door'):
        job_elements = get_job_list_handler(results_container, 'li', 'react-job-listing', 'glass.door')
    return (job_elements)

# aggregate function that grabs the job title per element found in the job list
def get_job_title(website, element):
    if (website == "monster"):
        title_element = element.find('h2', class_='title')
    if (website == "indeed"):
        title_element = element.find('a', class_="turnstileLink")
    if (website == "getting.hired"):
        title_element = element.find('h3', class_="c-job-stub__header b-link-colour")
        title_element = title_element.text.strip()
        title_element = re.sub(r'\s\s', "", title_element)
        title_element = re.sub(r'New', "", title_element)
        return (title_element)
    if (website == "flex.jobs"):
        title_element = element.find('a', class_="job-link")
    if (website == 'snag.a.job'):
        title_element = element.find('h3', class_="job__position")
    if (website == 'glass.door'):
        title_element_ = element.find('a', class_='jobInfoItem') #this needs fixin
        title_element = title_element_.find('span')
    if title_element != None:
        return (title_element.text.strip())

# Same but for location
def get_job_location(website, element, location):
    if (website == "monster"):
        location_element_raw = element.find('div', class_='location')
    if (website == "indeed"):
        location_element_raw = element.find('div', class_='location accessible-contrast-color-location')
    if (website == "getting.hired"):
        location_element_raw = element.find('dd', class_='c-properties-list__value')
    if (website == "flex.jobs"):
        return (f'{location[0]}')
    if (website == "snag.a.job"):
        location_element = element.find('div', class_="job--location").text.strip()
        try:
            location_element_extract = re.search(r'(?<=,\s).+(?=,)', location_element).group(0)
            return (location_element_extract)
        except AttributeError:
            return (location_element)
    if (website == 'glass.door'):
        location_element_raw = element.find('span', class_='loc')
    if (location_element_raw != None):
        location_element_full = location_element_raw.text.strip()
        try:
            location_element_full = re.search(r'.+?(?=,)', location_element_full).group(0)
        except AttributeError:
            location_element_full = "NA"
        finally:
            if (location_element_full != None):
                return (location_element_full)

# Same but for job company
def get_job_company(website, element):
    if (website == "monster"):
        company_element = element.find('div', class_='company')
    if (website == "indeed"):
        company_element = element.find('span', class_='company')
    if (website == "getting.hired"):
        company_element = element.find('p', class_='c-job-stub__recruiter')
    if (website == "flex.jobs"):
        company_element = element.find('a', class_="job-link")
    if (website == "snag.a.job"):
        company_element = element.find('h4', class_="job__company")
    if (website == 'glass.door'):
        company_element = element.find_all('a', class_ ='jobLink')
        for poss_element in company_element:
            poss_result_ = poss_element.find('span')
            if (poss_result_ == None):
                continue
            if (poss_result_.has_attr('class')):
                continue
            else:
                company_element = poss_result_
                break
    if (company_element != None):
        return (company_element.text.strip())

def get_link(website, element):
    if (website == "monster"):
        link_element = element.find('a')
        if (link_element != None):
            link_element = link_element['href']
    if (website == "indeed"):
        link_element = element.find('a')
        if (link_element != None):
            link_element = link_element['href']
            link_element = f'https://www.indeed.com{link_element}'
    if (website == "getting.hired"):
        link_element = element.find('a')
        if (link_element != None):
            link_element = link_element['href']
            link_element = f'https://www.getting.hired.com/{link_element}'
    if (website == "flex.jobs"):
        link_element = element.find('a', class_="job-link")
        if (link_element != None):
            link_element = link_element['href']
            link_element = f'https://flexjob.com{link_element}'
    if (website == "snag.a.job"):
        link_element = element.find(itemprop="url")
        if (link_element != None):
            link_element = re.search(r'(?<=content=").+(?="\s)', str(link_element)).group(0)
    if (website == 'glass.door'):
        link_element = element.find('a', class_='jobLink')
        if (link_element != None):
            link_element = link_element['href']
            link_element = f'https://www.glassdoor.com{link_element}'
    if (link_element != None):
        return (link_element)

# This appends the data that meets criteria into dataframe for export
def append_df(df, item1, item2, item3, item4):
    df = df.append({'Job Kind': item1, 'Job Title': item2, 'Company': item3, 'Link': item4}, ignore_index=True)
    return (df)

def reset_job_values():
    global url
    global page
    global soup
    url = None
    page = None
    soup = None

def reset_element_values():
    global job_details
    global location_details
    global company_details
    global link
    job_details = None
    location_details = None
    company_details = None
    link = None

def get_os():
    return (sys.platform)

def export_function(df):
    if (get_os() == 'win32'):
        print(f'Exporting files to C:/Users/{getpass.getuser()}/Documents/')
        print(f'File name: jobs_{str(datetime.date.today())}.csv')
        df.to_csv(
            f'C:/Users/{getpass.getuser()}/Documents/jobs_{datetime.date.today()}.csv', sep=",")
    else:
        print(f'Exporting file to Desktop. ')
        print(f'File name: jobs_{datetime.date.today()}.csv')
        df.to_csv(f'~/Desktop/jobs_{datetime.date.today()}.csv', sep=",")

def main():
    output_dataframe = pandas.DataFrame(columns=['Job Kind', 'Job Title', 'Company', 'Link'])
    websites = get_websites()
    print_website_list(websites)
    if (get_profession()):
        jobs = [which_profession()]
        while (multiple_professions_additional()):
            jobs.append(which_profession())
    else:
        jobs = ["None"]
    jobs = multiple_professions_redun_removal(jobs)
    print_job_list(jobs)
    location = get_location_main()
    search_amount = get_search_amount()
    for website in websites:
        if (website == 'glass.door'):
            glass_door_warning()
        for job_kind in jobs:
            found_amount = 0
            page_searched_amount = 0
            searched_amount = 0
            while found_amount < search_amount and searched_amount < 5:
                reset_job_values()
                print(f'Searching for {job_kind} on {website}. ')
                if (page_searched_amount == 0):
                    url = create_url(website, job_kind, location, True, page_searched_amount)
                else:
                    url = create_url(website, job_kind, location, False, page_searched_amount)
                page = call_url(website, url, job_kind)
                if (page == "404"):
                    print(f'No content for {job_kind} found on {website}. ')
                    break
                else:
                    page_searched_amount += 1
                soup = get_content(page)
                searched_amount += 1
                results = get_results_container(website, soup)
                job_elements = get_job_list(website, results)
                if (job_elements == False):
                    break
                for element in job_elements:
                    if (element == None):
                        pass
                    job_details = get_job_title(website, element)
                    location_detail = get_job_location(website, element, location)
                    company_details = get_job_company(website, element)
                    link = get_link(website, element)
                    # There is an issue with glass door and if there are no resutls found; how is this handled with the other websites and why cant it work with glassdoor?
                    if (location_detail == location[0]):
                        found_amount += 1
                        output_dataframe = append_df(output_dataframe, job_kind, job_details, company_details, link)
                    reset_element_values()
            print(f'Found {found_amount} for {job_kind} on {website}. ')
    export_function(output_dataframe)

if __name__ == '__main__':
    main()