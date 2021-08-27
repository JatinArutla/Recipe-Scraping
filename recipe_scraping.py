import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import pickle
import argparse

class creating_dataframe():

    def url_content(self, url):
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "lxml")
        return soup

    def cuisine(self, soup):
        e = []
        for li in soup.find_all('li', {"class":"collection-item avatar"}):
            for p in li.find('p'):
                e.append(p)
        return e

    def name_of_recipe(self, soup):
        for d in soup.find_all('div', {"class":"col s12 m12"}):
            for b in d.find_all('b'):
                recipe_name = b.text
            return recipe_name

    def nutrition_values(self, soup):        
        l = []
        for wrapper in soup.find_all('td', {"class":"roundOff"}):
            l.append(wrapper.text)
        return l

    def nutrition_labels(self, soup):
        k = []
        for wrapper in soup.find_all('strong'):
            k.append(wrapper.text)
        return k

    def instructions(self, soup):
        ins = []
        for p in soup.find_all('div', {"id":"steps"}):
            ins.append(p.text)
        return ins

    def link_of_source(self, soup):
        for li in soup.find_all('li', {"collection-item avatar"}):
            for a in li.find_all('a'):
                source_link = a.attrs['href']
        return source_link

    def name_of_ingredient(self, further_soup):
        for d in further_soup.find_all('div', {"class":"card-content"}):
            for b in d.find_all('b'):
                ingredient_name = b.text
        return ingredient_name

    def additional_headers(self, further_soup):
        further_header = []
        for t in further_soup.find_all('table', {"id":"myTable"}):
            for tr in t.find_all('tr'):
                for th in tr.find_all('th'):
                    further_header.append(th.text)
        return further_header

    def additional_values(self, further_soup):
        further_values = []
        for t in further_soup.find_all('table', {"id":"myTable"}):
            for tbody in t.find_all('tbody'):
                for tr in tbody.find_all('tr'):
                    for td in tr.find_all('td'):
                        further_values.append(td.text.strip())
        return further_values

    def forms_of_ingredients(self, soup):
        ing_nutrition = []
        for t in soup.find_all('table', {"class":"table striped"}):
            for tr in t.find_all('tr'):
                for td in tr.find_all('td'):
                    for a in td.find_all('a'):
                        if a.has_attr('href'):
                            ing_nutrition.append('https://cosylab.iiitd.edu.in' + a.attrs['href'])
        return ing_nutrition

    def data_of_ingredients(self, soup):
        ingredients = []
        for t in soup.find_all('table', {"class":"table striped"}):
            for tr in t.find_all('tr'):
                for td in tr.find_all('td'):
                    ingredients.append(td.text)
        return ingredients

    def save_to_csv(self, df, path):
        df.to_csv(path)

    def main(self):
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--starting_url",
                            default=None,
                            type=int,
                            help="Starting URL")

        parser.add_argument("--ending_url",
                            default=None,
                            type=int,
                            help="Ending URL")
        
        args = parser.parse_args()
        
        counter = 0
        df_nutrition = pd.DataFrame()
        df_ing = pd.DataFrame()
        # df_further_ing = pd.DataFrame()
        hyperlinks = []
        
        for i in range(args.starting_url, args.ending_url):
            time.sleep(0.5)
            recipe_id = str(i)
            url = f'https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/{i}'
            soup = self.url_content(url)
            e = self.cuisine(soup)

            if(e[0].strip() == 'Asian >> Indian Subcontinent >> Indian'):

                recipe_name = self.name_of_recipe(soup)
                l = self.nutrition_values(soup)
                k = self.nutrition_labels(soup)
                ins = self.instructions(soup)
                source_link = self.link_of_source(soup)

                temp = pd.DataFrame(columns=k[:154])
                a_series = pd.Series(l[:154], index = temp.columns)
                temp = temp.append(a_series, ignore_index=True)
                temp.insert(0, 'Recipe name', recipe_name)
                temp.insert(1, 'Recipe ID', recipe_id)
                temp.insert(2, 'Cuisine_X', e[0].strip())
                temp.insert(3, 'Instructions', ins[0].strip().replace('\t', '').replace('|', '').replace('-', '').strip())
                temp.insert(4, 'Prep and Cook time', e[2].strip())
                temp.insert(5, 'Source link', source_link)

                df_nutrition = df_nutrition.append(temp, ignore_index=True)

                ingredients = self.data_of_ingredients(soup)
                fin_ing = []
                c = 8
                b = 0
                sub = []
                for p in range(int(len(ingredients)/8)):
                    for j in range(b, c):
                        sub.append(ingredients[j])
                    fin_ing.append(sub)
                    sub = []
                    b+=8
                    c+=8

                temp = pd.DataFrame(fin_ing)
                temp.columns = ['Ingredient Name', 'Quantity', 'Unit', 'State', 'Energy (kcal)', 'Carbohydrates', 'Protein (g)', 
                                 'Total Lipid (Fat) (g)']
                temp = temp.astype(str)
                temp.replace('1/2', '0.5', inplace=True)
                temp.replace('1/4', '0.25', inplace=True)
                temp.replace('1/8', '0.125', inplace=True)
                temp.insert(0, 'Recipe ID', recipe_id)

                ing_nutrition = self.forms_of_ingredients(soup)
                hyperlinks.append(ing_nutrition)
                
                temp['Links of Forms'] = ing_nutrition

                df_ing = df_ing.append(temp, ignore_index=True)
                    
            counter+=1
            # if (counter % 2000 == 0):
            self.save_to_csv(df_nutrition, 'Nutrition.csv')
            self.save_to_csv(df_ing, 'Ingredients.csv')
            
            f_name = 'hyperlinks.pkl'
            open_file = open(f_name, "wb")
            pickle.dump(hyperlinks, open_file)
            open_file.close()

            if (counter % 200 == 0):
                print(f'{counter} recipes checked')

if __name__ == "__main__":
    func = creating_dataframe()
    func.main()
