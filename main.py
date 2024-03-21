import re
import os
#import git
import json
import requests
import tkinter as tk
from tkinter import simpledialog
import config
from bs4 import BeautifulSoup
from mdutils.mdutils import MdUtils

path = config.path

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
    clean = clean.replace("&lt;", "<=")
    clean = clean.replace("&gt;", ">=")
    clean = clean.replace("&quot;", "\"")

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
                print("Invalid problem name, check spelling and try again")
                main()
                
            print("Error, status code: " + response.status_code)
            main()
        
    #handle exceptions: bad urls or no internet
    except requests.RequestException as e:
        return f"{str(e)}"
    
def add_problem(name, language, description, solution):

    #check if repo exists, if not create it
    if os.path.exists(path):
        repo = git.Repo(path)
    else:
        return f"No repository found. Create a git repository and add the path to config.py or as the local path variable. \n (It is reccomended to not publish your path)"

    problem_path = path + '/' + name
    if not os.path.exists(problem_path):
        os.mkdir(problem_path)
        print(problem_path, "created!")

    #add language subfolder
    language_path = problem_path + '/' + language
    if not os.path.exists(language_path):
        os.mkdir(language_path)
        print(language_path, "created!")

    #store the problem description and solution in a markdown file
    md_title = name + " " + language + " " + 'Solution'
    md_path = os.path.join(language_path, 'solution')
    md = MdUtils(file_name=md_path, title=md_title)
    md.new_paragraph(description, 'i')
    md.insert_code(solution, language)
    md.create_md_file()
    return


def main():
    def problem_input():
        nonlocal problem_name
        problem_name = entry.get()
        window.destroy()
    
    def language_input():
        nonlocal language
        language = entry.get()
        window.destroy()
        
    def solution_input():
        nonlocal solution
        solution = text_box.get("1.0", tk.END)
        window.destroy()
        
    window = tk.Tk()
    label = tk.Label(text="What problem did you solve?")
    entry = tk.Entry()
    button = tk.Button(text="Submit", command=problem_input)
    
    label.pack()
    entry.pack()
    button.pack()
    window.mainloop()
    problem_name = problem_name.lower()
    
    
    window = tk.Tk()
    label = tk.Label(text="What language did you use?")
    entry = tk.Entry()
    button = tk.Button(text="Submit", command=language_input)   
    
    label.pack()
    entry.pack()
    button.pack()
    window.mainloop()
    language = language.lower()

    
    window = tk.Tk()
    label = tk.Label(text="Copy and paste your solution:")
    text_box = tk.Text()
    button = tk.Button(text="Submit", command=solution_input)
    
    label.pack()
    text_box.pack()
    button.pack()
    window.mainloop()
    
    solution = solution

    url = generate_url(problem_name)
    description = get_problem_data(url)
    
    print(problem_name)
    print(language)
    print(description)
    print(solution)

    add_problem(problem_name, language, description, solution)
    
main()


