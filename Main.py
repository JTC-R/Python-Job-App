import requests
from bs4 import BeautifulSoup
import pandas
import re
import datetime
import sys
import getpass

def get_websites():
    chosen_website = []
    possible_website = ['monster', 'indeed', 'getting.hired', 'flex.jobs', 'snag.a.job']
    possible_yes = ['yes', 'Yes', 'y', 'Y']
    possible_no = ['no', 'No', 'n', 'N']
    answer_one = input("Do you want to search all websites? (Yes/No) ")
    if(answer_one in possible_yes):
        chosen_website = possible_website
        print(f'Searching websites {chosen_website}.')
        return(chosen_website)
    elif (answer_one not in possible_no):
        while(answer_one not in possible_yes and answer_one not in possible_no):
            print("Please answer Yes or No")
            answer_one = input("Do you want to search all websites? (Yes/No) ")
        if(answer_one in possible_yes):
            chosen_website = possible_website
            return(chosen_website)
        elif(answer_one in possible_no):
            for website in possible_website:
                answer = input("Do you want to search " + website + "? ")
                if (answer in possible_yes):
                    chosen_website.append(website)
                elif (answer not in possible_no):
                    while (answer not in possible_yes and answer not in possible_no):
                        print("Please answer Yes or No ")
                        answer = input("Do you want to search " + website + "? ")
    else:
        for website in possible_website:
            answer = input("Do you want to search " + website + "? ")
            if(answer in possible_yes):
                chosen_website.append(website)
            elif(answer not in possible_no):
                while(answer not in possible_yes and answer not in possible_no):
                    print("Please answer Yes or No ")
                    answer = input("Do you want to search " + website + "? ")
    print(f'Searching websites {chosen_website}.')
    return(chosen_website)

def get_profession():
    possible_yes = ['yes', 'Yes', 'y']
    possible_no = ['no', 'No', 'n']
    answer = input("Do you want to search a specific job type? (Yes/No) ")
    while(answer not in possible_yes and answer not in possible_no):
        print("Please answer with Yes or No ")
        answer = input("Do you want to search a specific job type? (Yes/No) ")
    if(answer in possible_yes):
        return(True)
    else:
        return(False)

def which_profession():
    answer = input("Which job type of job do you want to look for? ")
    while(re.search(r'\d', answer)):
        print("Please re-input the type of job ")
        answer = input("Which type of job do you want to look for? ")
    return(answer)

def multiple_professions():
    answer = input("Do you want to search multiple jobs? (Yes/No) ")
    if(answer == "Yes" or answer == "yes"):
        return(True)
    else:
        return(False)

def multiple_professions_additional():
    possible_yes = ['yes', 'Yes', 'y']
    possible_no = ['no', 'No', 'n']
    changed_mind = [' ']
    answer = input("Do you want to add an additional job? (Yes/No) ")
    while(answer not in possible_yes and answer not in possible_no and answer not in changed_mind):
        print("Please answer with Yes or No or press 'Enter' if you wish to skip. ")
        answer = input("Do you want to add an additional job? (Yes/No) ")
    if(answer in possible_yes):
        return(True)
    else:
        return(False)

def multiple_professions_redun_removal(input):
    return(list(set(input)))

def print_job_list(jobs):
    print("The jobs being searched for are: " + str(jobs))

def get_location():
    location = "Philadelphia"
    return(location)

def create_monster(job, location, new):
    base_url = "http://www.monster.com"
    location = str(location) + "__2C-PA"
    if(job == "None"):
        full_url = base_url + "/jobs/search/?where=" + location
    else:
        job = re.sub(r'\s', '-', job)
        full_url = base_url + "/jobs/search/?q=" + job + "&where=" + location
    if(new == False):
        full_url = full_url + "&stpage=1&page=2"
    return(full_url)

def create_indeed_url(job, location, new):
    base_url = "http://www.indeed.com"
    location = str(location) + ",+PA"
    if(job == "None"):
        full_url = base_url + "/jobs?l=" + location
    else:
        job = re.sub(r'\s', '+', job)
        full_url = base_url + "/jobs?q=" + job + "&l=" + location
    if(new == False):
        full_url = full_url + "&start=10"
    return(full_url)

def create_zip_url(job, location, new):
    base_url = "http://www.ziprecruiter.com"
    location = str(location) + "%2C+PA"
    if(job == 'None'):
        full_url = base_url + "/candidate/search?search=&location=" + location
    else:
        job = re.sub(r'\s', '+', job)
        full_url =  base_url + "/candidate/search?radius=25&search=" + job + "&location=" + location
    if(new == False):
        full_url = full_url + "&page=2"
    return(full_url)

def create_gettinghired_url(job, location, new):
    base_url = "http://www.gettinghired.com/jobs/"
    location = location
    if(job == "None"):
        full_url = base_url + location + "/"
    else:
        job = re.sub(r'\s', '-', job)
        full_url = base_url + location + "/?kw=" + job
    if(new == False):
        full_url = full_url + "&ix=20"
    return(full_url)

def create_flexjobs_url(job, location, new):
    base_url = "http://www.flexjobs.com"
    location = location + "%C+PA"
    if(job == "None"):
        full_url = base_url + "/search?search=&search=&location=" + location
    else:
        job = re.sub(r'\s', '+', job)
        full_url = base_url + "/search?search=" + job + "&location=" + location
    return(full_url)

def create_snagajob_url(job):
    base_url = "http://www.snagajob.com/"
    location = "19148"
    if(job == "None"):
        full_url = base_url + "search?w=" + location + "&radius=5"
    else:
        job = re.sub(r'\s', '+', job)
        full_url = base_url + "search?q=" + job + "&w=" + location + "&radius=5"
    return(full_url)

def create_url(website, job, location, new):
    if(website == 'monster'):
        url = create_monster(job, location, new)
    elif(website == 'indeed'):
        url = create_indeed_url(job, location, new)
    elif(website == 'zip'):
        url = create_zip_url(job, location, new)
    elif(website == 'getting.hired'):
        url = create_gettinghired_url(job, location, new)
    elif(website == "flex.jobs"):
        url = create_flexjobs_url(job, location, new)
    elif(website == "snag.a.job"):
        url = create_snagajob_url(job)
    return(url)

def call_url(website, full_url, job):
    if(website == 'zip'):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                   'sec-ch-ua' : 'Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87',
                   'Referer' : 'https://www.ziprecruiter.com/candidate/search?search=&location=Philadelphia%2C+PA',
                   'sec-ch-ua-mobile': '?0'}
        page = requests.get(full_url, headers = headers)
    else:
        page = requests.get(full_url)
    if(page.status_code == 200):
        return(page)
    else:
        print(f"Unable to obtain website {website} for job {job}. ")
        return("404")

def get_content(page):
    if(page != "None"):
        try:
            soup = BeautifulSoup(page.content, 'html.parser')
            return (soup)
        except AttributeError:
            return(False)

def get_results_container(website, soup):
    if(website == "monster"):
        results = soup.find(id ='ResultsContainer')
    if(website == "indeed"):
        results = soup.find(id = 'resultsCol')
    if(website == "getting.hired"):
        results = soup.find(id = 'listing')
    if(website == "flex.jobs"):
        results = soup.find(id = 'joblistarea')
    if(website == "snag.a.job"):
        results = soup.find('div', class_ ="results")
    return (results)

def get_job_list_handler(container, parent, child, website):
    try:
        if(website != 'indeed' and website != 'snag.a.job'):
            job_elements = container.find_all(parent, class_ = child)
        elif(website == 'snag.a.job'):
            job_elements = container.find_all(parent)
        else:
            job_elements = container.find_all(parent, attrs_ = child)
    except AttributeError:
        print(f'No job container on {website}.')
        job_elements = False
    return(job_elements)

def get_job_list(website, results_container):
    if(website == "monster"):
        job_elements = get_job_list_handler(results_container, 'section', 'card-content', 'monster')
    elif(website == "indeed"):
        job_elements = get_job_list_handler(results_container, 'div', {'class':'jobsearch-SerpJobCard unifiedRow row result'}, 'indeed')
    elif(website == "getting.hired"):
        job_elements = get_job_list_handler(results_container, 'li', 'c-lister__item', 'getting.hired')
    elif(website == "flex.jobs"):
        job_elements = get_job_list_handler(results_container, 'li', 'list-group-item job', 'flex.jobs')
    elif(website == "snag.a.job"):
        job_elements = get_job_list_handler(container = results_container, parent = 'job-overview', website = 'snag.a.job', child = None)
    return(job_elements)

def get_job_title(website, element):
    if(website == "monster"):
        title_element = element.find('h2', class_='title')
    if(website == "indeed"):
        title_element = element.find('a', class_="turnstileLink")
    if(website == "getting.hired"):
        title_element = element.find('h3', class_="c-job-stub__header b-link-colour")
        title_element = title_element.text.strip()
        title_element = re.sub(r'\s\s', "", title_element)
        title_element = re.sub(r'New', "", title_element)
        return(title_element)
    if(website == "flex.jobs"):
        title_element = element.find('a', class_ = "job-link")
    if(website == 'snag.a.job'):
        title_element = element.find('h3', class_="job__position")
    if title_element != None:
        return(title_element.text.strip())

def get_job_location(website, element):
    if(website == "monster"):
        location_element_raw = element.find('div', class_='location')
    if(website == "indeed"):
        location_element_raw = element.find('div', class_='location accessible-contrast-color-location')
    if(website == "getting.hired"):
        location_element_raw = element.find('dd', class_='c-properties-list__value')
    if(website == "flex.jobs"):
        return("Philadelphia")
    if(website == "snag.a.job"):
        location_element = element.find('div', class_="job--location").text.strip()
        try:
            location_element_extract = re.search(r'(?<=,\s).+(?=,)', location_element).group(0)
            return(location_element_extract)
        except AttributeError:
            return(location_element)
    if(location_element_raw != None):
        location_element_full = location_element_raw.text.strip()
        try:
            location_element = re.search(r'.+?(?=,)', location_element_full).group(0)
        except AttributeError:
          location_element = "NA"
        finally:
            if(location_element != None):
                return(location_element)

def get_job_company(website, element):
    if(website == "monster"):
        company_element = element.find('div', class_='company')
    if(website == "indeed"):
        company_element = element.find('span', class_='company')
    if(website == "getting.hired"):
        company_element = element.find('p', class_='c-job-stub__recruiter')
    if(website == "flex.jobs"):
        company_element = element.find('a', class_="job-link")
    if(website == "snag.a.job"):
        company_element = element.find('h4', class_="job__company")
    if (company_element != None):
        return (company_element.text.strip())

def get_link(website, element):
    if(website == "monster"):
        link_element = element.find('a')
        if(link_element != None):
            link_element = link_element['href']
    if(website == "indeed"):
        link_element = element.find('a')
        if(link_element != None):
            link_element = link_element['href']
            link_element = "https://www.indeed.com" + link_element
    if(website == "getting.hired"):
        link_element = element.find('a')
        if(link_element != None):
            link_element = link_element['href']
            link_element = "http://www.getting.hired.com/" + link_element
    if(website == "flex.jobs"):
        link_element = element.find('a', class_ = "job-link")
        if(link_element != None):
            link_element = link_element['href']
            link_element = "http://flexjobs.com" + link_element
    if(website == "snag.a.job"):
        link_element = element.find(itemprop="url")
        if(link_element != None):
            link_element = re.search(r'(?<=content=").+(?="\s)', str(link_element)).group(0)
    if(link_element != None):
        return(link_element)

def append_df(df, item1, item2, item3, item4):
    df = df.append({'Job Kind' : item1, 'Job Title' : item2, 'Company' : item3, 'Link' : item4}, ignore_index = True)
    return(df)

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
    return(sys.platform)

def main():
    output_dataframe = pandas.DataFrame(columns = ['Job Kind','Job Title' , 'Company' , 'Link'])
    websites = get_websites()
    if(get_profession()):
        jobs = [which_profession()]
        while(multiple_professions_additional()):
            jobs.append(which_profession())
    else:
        jobs = ["None"]
    jobs = multiple_professions_redun_removal(jobs)
    print_job_list(jobs)
    location = get_location()
    for website in websites:
        for job_kind in jobs:
            reset_job_values() #added to reset the values
            print("Searching for " + str(job_kind) + " on " + str(website))
            amount = 0
            url = create_url(website, job_kind, location, True)
            page = call_url(website, url, job_kind)
            if(page == "404"):
                break
            soup = get_content(page)
            if(soup == False):
                print(f'No content found on {website} for {job_kind}. ')
                break
            else:
                results = get_results_container(website, soup)
                job_elements = get_job_list(website, results)
                if(job_elements == False):
                    break
                for element in job_elements:
                    if(element == None):
                        pass
                    job_details = get_job_title(website, element)
                    location_detail = get_job_location(website, element)
                    company_details = get_job_company(website, element)
                    link = get_link(website, element)
                    if(location_detail == "Philadelphia"):
                        amount += 1
                        output_dataframe = append_df(output_dataframe, job_kind, job_details, company_details, link)
                    job_details = None
                    location_detail = None
                    company_details = None
                    link = None
                if(amount < 10):
                    url_extended = create_url(website, job_kind, location, False)
                    page_extended = call_url(website, url_extended, job_kind)
                    if(page_extended == "404"):
                        break
                    soup = get_content(page_extended)
                    if(soup == False):
                        print(f'No content found on {website} for {job_kind} on the second page. ')
                        break
                    results = get_results_container(website, soup)
                    job_elements = get_job_list(website, results)
                    if(job_elements == False):
                        break
                    for element in job_elements:
                        if(element == None):
                            pass
                        job_details = get_job_title(website, element)
                        location_details = get_job_location(website, element)
                        company_details = get_job_company(website, element)
                        link = get_link(website, element)
                        if (location_details == "Philadelphia"):
                            amount += 1
                            output_dataframe = append_df(output_dataframe, job_kind, job_details, company_details, link)
                reset_element_values()
                print("Found " + str(amount) + " on " + str(website) + " for " + str(job_kind))
    print("Exporting data to desktop")
    place = get_os()
    if(place == 'win32'):
        print(f'Exporting files to C:/Users/{getpass.getuser()}/Documents/')
        print(f'File name: jobs_{str(datetime.date.today())}.csv')
        output_dataframe.to_csv('C:/Users/'+ getpass.getuser() + '/Documents/jobs_' + str(datetime.date.today()) + '.csv', sep=",")
        #output_dataframe.to_csv('C:/Users/justi/OneDrive/Documents/Python/Jobs/jobs_' + str(datetime.date.today()) +'.csv', sep=",")
    else:
        print(f'Exporting file to Desktop. ')
        print(f'File name: jobs_{datetime.date.today()}.csv')
        output_dataframe.to_csv("~/Desktop/jobs_" + str(datetime.date.today()) +'.csv', sep=",")

if __name__ == '__main__':
    main()
