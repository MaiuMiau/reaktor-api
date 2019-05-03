from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import csv

DEBUG = True

# def main():
#     with open('./paastokansio/paastot.csv','r') as paastot:
#             readCSV = csv.reader(paastot, delimiter=',')
#             #country = input("from what country do you want info? ")
#             #inputyear = input("For what year do you want info? ")
#             country = 'Finland'
#             inputyear = '1961'
#             headers=[]
#             countries=[]
#             data=[]
#             #loop trough rows in file
#             for row in readCSV:
#                 numOfLines = readCSV.line_num
#                 #We dont need the fist 4 lines
#                 #Line 5 is headers. We can find
#                 if numOfLines == 5:
#                     headers = row
#                     print(headers)
#                     indexY = headers.index(inputyear)
#                     year = row[indexY]
#                     print(year)
#                     data.append(year)
#                 elif numOfLines > 5:
#                     #add all countruNames to list
#                    countries.append(row[0])
#                    #find selected country and co2emissions from selected year
#                    if row[0] == country :
#                        chosenCountry = row[0]
#                        data.append(chosenCountry)
#                        print(country + " CO2 emissions in the year: " + inputyear)
#                        emissions = row[indexY]
#                        data.append(emissions)
# main()

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

#function to get pupulation array based on country
def getPeople(country):
    print(country)
    with open('./vakilukukansio/vakiluku.csv','r') as vakiluvut:
             readCSV = csv.reader(vakiluvut, delimiter=',')
             for row in readCSV:
                 numOfLines = readCSV.line_num
                 #first rows are not needed
                 if numOfLines > 5:
                    #find selected country and population row
                    if row[0] == country:
                        result = row[5:]
                        print(result)
    return result

# get coutry names to array so that they can be used
# in frontend dropdown form
@app.route('/getcountries', methods=['GET'])
def getCountries():
    with open('./paastokansio/paastot.csv','r') as paastot:
             readCSV = csv.reader(paastot, delimiter=',')
             countries=[]
             #loop trough rows in file
             for row in readCSV:
                 numOfLines = readCSV.line_num
                 if numOfLines > 5:
                     countries.append(row[0])
    return jsonify({'countries': countries} )

@app.route('/getemissions', methods=['POST', 'GET'])
def getData():
        post_data = request.get_json()
        country  = post_data['country']
        #country  = "Finland"
        print(country )
        with open('./paastokansio/paastot.csv','r') as paastot, open('./vakilukukansio/vakiluku.csv','r') as vakiluvut:
                 readCSV = csv.reader(paastot, delimiter=',')
                 readVakiluvut = csv.reader(vakiluvut, delimiter=',')
                 emissions=[]
                 years=[]
                 results =[]
                 population=[]
                 population= getPeople(country)
                 #loop trough rows in file
                 for row in readCSV:
                     numOfLines = readCSV.line_num
                     #We dont need the fist 4 lines
                     #Line 5 is headers
                     if numOfLines == 5:
                         #read years to array
                         years = (row[5:])
                     elif numOfLines > 5:
                        #find selected country and co2emissions
                        if row[0] == country:
                            emissions = (row[5:])
                            #check how many times we have to loop
                            loops = len(row[5:])
                            #loop trough both arrays
                            for i in range(loops):
                                year = years[i]
                                emission = emissions[i]
                                people = population[i]
                                if emission != '':
                                    percapita = float(emission) / int(people)
                                elif emission == '':
                                    emission = '-'
                                    percapita = 0.0
                                # constructin result object
                                result = {'year': year, 'emission': emission, 'percapita': percapita}
                                #add resultobject to array
                                results.append(result)
                                print(result)
                            return jsonify({'results': results})

if __name__ == '__main__':
    app.run()
