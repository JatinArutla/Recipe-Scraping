# Recipe-Scraping
 
## Cloning
``` git clone https://github.com/JatinArutla/Recipe-Scraping.git ```      
``` cd Recipe-Scraping ```

## Prerequisites
Install the following:
* Start by installing virtualenv if you don't have it: ``` pip install virtualenv ```
* Once installed access the project folder: ``` cd Recipe-Scraping ```
* Create a virtual environment: ``` virtualenv VirtualEnv ```
* Enable the virtual environment: ``` source VirtualEnv/bin/activate ```
* Install the python dependencies on the virtual environment: ``` pip install -r requirements.txt ```

## Web Scraping and Creating a CSV file
Returns CSV files for the Recipe Nutrition data, Recipe Ingredient data and a Pickle file for the Forms of Ingredient data
### Usage:
``` python3 recipe_scraping.py --starting_url <starting_url> --ending_url <ending_url> ```      
--starting_url -- The ID of the Recipe that we start the scraping from    
--ending_url -- The ID of the Recipe that we end the scraping at       
ex: ``` python3 recipe_scraping.py --starting_url 4003 --ending_url 4010 ```
