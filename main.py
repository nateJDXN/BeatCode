import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

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


def get_problem_data(url):
    #check url integrity and grab description if successful
    try:
        #send a GET request to the URL
        response = requests.get(url)
        #check response
        if response.status_code == 200:
            
            #if successful, parse HTML - problem description in "description" meta tag
            soup = BeautifulSoup(response.text, 'lxml')
            #find head tag
            head_tag = soup.find('head')
            if head_tag:
                #find description meta tag
                description_tag = head_tag.find('meta', attrs={'name': 'description'})
                if description_tag:
                    #description found, return content
                    return description_tag.get('content')
                else:
                    return f"<meta name='description'> not found"
            else:
                return f"<head> not found"
        else:
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


