from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import csv


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

#function to get pupulation based on country an year
def getPeople(indexY, country):
    print(indexY)
    print(country)
    with open('./vakilukukansio/vakiluku.csv','r') as vakiluvut:
             readCSV = csv.reader(vakiluvut, delimiter=',')
             for row in readCSV:
                 numOfLines = readCSV.line_num
                 #first rows are not needet
                 if numOfLines > 5:
                    #find selected country and population from selected year
                    if row[0] == country:
                        result = row[indexY]
                        print(result)
    return result

# get coutry names and years to arrays so that they can be used
# in frontend dropdown form
@app.route('/getcountries')
def getCountries():
    with open('./paastokansio/paastot.csv','r') as paastot:
             readCSV = csv.reader(paastot, delimiter=',')
             countries=[]
             data=[]
             years=[]
             #loop trough rows in file
             for row in readCSV:
                 numOfLines = readCSV.line_num
                 if numOfLines == 5:
                    del row[0:4]
                    row.reverse()
                    del row[0:1]
                    years.append(row)
                 elif numOfLines > 5:
                     countries.append(row[0])
    return jsonify({'countries': countries, 'years': years} )

@app.route('/getemissions', methods=['POST', 'GET'])
def getData():
        #d = request.form
        #print(d)
        #print(request.get_json())
        post_data = request.get_json()
        country  = post_data['country']
        inputyear  = post_data['year']
        checkbox  = post_data['perCapita']
        print(country )
        with open('./paastokansio/paastot.csv','r') as paastot, open('./vakilukukansio/vakiluku.csv','r') as vakiluvut:
                 readCSV = csv.reader(paastot, delimiter=',')
                 readVakiluvut = csv.reader(vakiluvut, delimiter=',')
                 countries=[]
                 data=[]
                 #loop trough rows in file
                 for row in readCSV:
                     numOfLines = readCSV.line_num
                     #We dont need the fist 4 lines
                     #Line 5 is headers. get index of input year
                     if numOfLines == 5:
                         indexY = row.index(inputyear)
                         year = row[indexY]
                         #print(year)
                         data.append(year)
                     elif numOfLines > 5:
                        #find selected country and co2emissions from selected year
                        if row[0] == country:
                            chosenCountry = row[0]
                            data.append(chosenCountry)
                            emissions = row[indexY]
                            data.append(emissions)
                            if checkbox == "show":
                                capita= getPeople(indexY, country)
                                print(capita)
                                if emissions != "" and capita != "":
                                    percapita = float(emissions) / float(capita)
                                    print(percapita)
                                    data.append(percapita)
                                    print(data)
                            print(country + " CO2 emissions in the year: " + inputyear)
                            return jsonify({'data': data})

if __name__ == '__main__':
    app.run()
