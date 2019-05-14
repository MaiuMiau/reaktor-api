from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import csv

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

#function to get pupulation array based on country
def getPeople(country):
    with open('./vakilukukansio/vakiluku.csv','r') as vakiluvut:
             readCSV = csv.reader(vakiluvut, delimiter=',')
             for row in readCSV:
                 numOfLines = readCSV.line_num
                 #first rows are not needed
                 if numOfLines > 5:
                    #find selected country and population row
                    if row[0] == country:
                        result = row[4:-1]
    return result
#function to get emissions for first selected country
def getEmissionsFor1(country1, checkbox):
        emissions1 = []
        emissionspercapita = []
        with open('./paastokansio/paastot.csv','r') as paastot:
                 readCSV = csv.reader(paastot, delimiter=',')
                 #loop trough rows in file
                 for row in readCSV:
                     numOfLines = readCSV.line_num
                     #dont need the fist 5 lines
                     #after line 5 check if line starts with selected country
                     if numOfLines > 5:
                        #find selected countries and co2emissions
                        if row[0] == country1:
                            emissions1 = row[4:-1]
        #if checkbox is True calculate emissions  percapita
        if checkbox == True:
            #function to get pupulation array based on country
            population= getPeople(country1)
            #check how many times we have to loop
            loops = len(emissions1)
             #loop trough both arrays
            for i in range(loops):
                #check if there is any empty values in arrays
                if emissions1[i] != '' and population[i] != '':
                    percapita = float(emissions1[i]) / int(population[i])
                    percapita = format(percapita, ".5f")
                    emissionspercapita.append(percapita)
                if population[i] != '' and emissions1[i] == '':
                    emissions1[i] = 0
                    percapita = float(emissions1[i]) / int(population[i])
                    percapita = format(percapita, ".5f")
                    emissionspercapita.append(percapita)
                elif population[i] == '':
                    population[i] = 0
                    emissions1[i] = 0
                    percapita = 0.0
                    percapita = format(percapita, ".5f")
                    emissionspercapita.append(percapita)
            #change country emission values to percapita values
            emissions1 = emissionspercapita
        result = emissions1
        return result
#function to get emissions for second selected country
def getEmissionsFor2(country2, checkbox):
        emissions2 = []
        emissionspercapita = []
        with open('./paastokansio/paastot.csv','r') as paastot:
                 readCSV = csv.reader(paastot, delimiter=',')
                 for row in readCSV:
                     numOfLines = readCSV.line_num
                     #dont need the fist 5 lines
                     if numOfLines > 5:
                        #after line 5 check if line starts with selected country
                        #find selected countries and co2emissions
                        if row[0] == country2:
                            emissions2 = row[4:-1]
        #if checkbox is True calculate emissions  percapita
        if checkbox == True:
            #function to get pupulation array based on country
            population= getPeople(country2)
            #check how many times we have to loop
            loops = len(emissions2)
             #loop trough both arrays
            for i in range(loops):
                 #check if there is any empty values in arrays
                if emissions2[i] != '' and population[i] != '':
                    percapita = float(emissions2[i]) / int(population[i])
                    percapita = format(percapita, ".5f")
                    emissionspercapita.append(percapita)
                if population[i] != '' and emissions2[i] == '':
                    emissions2[i] = 0
                    percapita = float(emissions2[i]) / int(population[i])
                    percapita = format(percapita, ".5f")
                    emissionspercapita.append(percapita)
                elif population[i] == '':
                    population[i] = 0
                    emissions2[i] = 0
                    percapita = 0.0
                    percapita = format(percapita, ".5f")
                    emissionspercapita.append(percapita)
            emissions2 = emissionspercapita
        result = emissions2
        return result

# get coutry names to array so that they can be used
# in frontend dropdown datalist
@app.route('/getcountries', methods=['GET'])
def getCountries():
    with open('./paastokansio/paastot.csv','r') as paastot:
             readCSV = csv.reader(paastot, delimiter=',')
             countries=[]
             #loop trough rows in file
             for row in readCSV:
                 numOfLines = readCSV.line_num
                 #dont need to check the fist 5 lines
                 if numOfLines > 5:
                     #row[0] = country names
                     #read all the names to array
                     countries.append(row[0])
    return jsonify({'countries': countries} )

#compare emissions when two countries are selected
@app.route('/emissionscompare', methods=['POST', 'GET'])
def compareData():
        post_data = request.get_json()
        country1 = post_data['form']['country']
        country2 = post_data['form']['country2']
        checkbox = post_data['percapita']

        #variables
        emissions1 = []
        emissions2 = []
        years = []
        results = []

        #functions to get emission based on country
        emissions1 = getEmissionsFor1(country1, checkbox)
        emissions2 = getEmissionsFor2(country2, checkbox)
        #open esmission CSV file to get years
        with open('./paastokansio/paastot.csv','r') as paastot:
                 readCSV = csv.reader(paastot, delimiter=',')
                 for row in readCSV:
                     numOfLines = readCSV.line_num
                     #We dont need the fist 4 lines
                     #Line 5 is headers
                     if numOfLines == 5:
                         #read years to array
                         years = row[4:-1]
        result = {'country': country1, 'emissions': emissions1}
        #add resultobject to array
        results.append(result)
        result = {'country': country2, 'emissions': emissions2}
        #add resultobject to array
        results.append(result)
        return jsonify({'results': results, 'years': years})

#get emissions when one country is selected
@app.route('/getemissions', methods=['POST', 'GET'])
def getData():
        post_data = request.get_json()
        country1 = post_data['form']['country']
        country2 = post_data['form']['country2']
        checkbox = post_data['percapita']
        country = ''
        #check which input field was used
        if country1 == '':
            country = country2
        if country2 == '':
            country = country1
        #open esmission CSV file
        with open('./paastokansio/paastot.csv','r') as paastot:
                 readCSV = csv.reader(paastot, delimiter=',')
                 #variables
                 emissions=[]
                 years=[]
                 population=[]
                 emissionspercapita = []
                 #loop trough rows in file
                 for row in readCSV:
                     numOfLines = readCSV.line_num
                     #We dont need the fist 4 lines
                     #Line 5 is years
                     if numOfLines == 5:
                         #read years to array
                         years = row[4:-1]
                     #after line 5 check if line starts with selected country
                     elif numOfLines > 5:
                        #find selected country and co2emissions
                        if row[0] == country:
                            emissions = row[4:-1]
        #if checkbox is True calculate emissions  percapita
        if checkbox == True:
            #function to get pupulation array based on country
            population= getPeople(country)
        #check how many times we have to loop
            loops = len(years)
            #loop trough both arrays
            for i in range(loops):
                #check if there is any empty values in arrays
                if emissions[i] != '' and population[i] != '':
                    percapita = float(emissions[i]) / int(population[i])
                    percapita = format(percapita, ".5f")
                    emissionspercapita.append(percapita)
                if population[i] != '' and emissions[i] == '':
                    emissions[i] = 0
                    percapita = float(emissions[i]) / int(population[i])
                    percapita = format(percapita, ".5f")
                    emissionspercapita.append(percapita)
                elif population[i] == '':
                    population[i] = 0
                    emissions[i] = 0
                    percapita = 0.0
                    percapita = format(percapita, ".5f")
                    emissionspercapita.append(percapita)
            #change country emission values to percapita values
            emissions = emissionspercapita
        result = {'country': country, 'emissions': emissions}
        return jsonify({'result': result, 'years': years})

if __name__ == '__main__':
    app.run()
