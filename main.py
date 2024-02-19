import re
import json
import requests
from bs4 import BeautifulSoup
from github import GitHub

def generate_url(problem_name):
    url = "https://leetcode.com/problems/"
    #replace spaces with "-"
    for char in problem_name:
        if char == " ":
            char = "-"
        url += char
    url += "/"
    #print(url)
    return url

def clean_data(data):
    clean = re.sub(r'<[^>]*>', '', data)
    clean = clean.replace("&nbsp;", "")
    return clean


def get_problem_data(url):
    #check url integrity and grab description if successful
    try:
        #send a GET request to the URL
        response = requests.get(url)
        #check response
        if response.status_code == 200:
            
            #save lxml file
            soup = BeautifulSoup(response.text, 'lxml')

            #dump lxml file
            ''' 
            f = open("soupfile.txt", "a")
            f.write(str(soup))
            print(soup) '''

            #get __NEXT_DATA__ script tag (contains JSON content)
            script_tag = soup.find('script', attrs={'id': '__NEXT_DATA__'})
            if script_tag:
                #parse JSON data
                data = json.loads(script_tag.string)

                #dump JSON data
                f = open("data/description_json.txt", "a")
                f.write(str(json.dumps(data, indent=4)))

                #return description
                data = data.get('props', {}).get('pageProps', {}).get('dehydratedState', {}).get('queries', [{}])[7].get('state', {}).get('data', {}).get('question', {}).get('content', '')
                
                #clean data
                description = clean_data(data)
                 
                # print(description)
                return description

        else:
            if response.status_code == 404:
                return f"Invalid problem name, check spelling and try again"
            return f"Error, status code: {response.status_code}"
    #handle exceptions: bad urls or no internet
    except requests.RequestException as e:
        return f"{str(e)}"
    


def main():
    problem_name = input("What problem did you solve?").lower()
    url = generate_url(problem_name)
    description = get_problem_data(url)
    print(description)
    
main()


