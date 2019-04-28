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

@app.route('/getemissions', methods=['POST', 'GET'])
def getData():
        d = request.form.to_dict()
        print(d)
        post_data = request.get_json()
        country  = post_data['formData']['country']
        inputyear  = post_data['formData']['year']
        print(country )
        with open('./paastokansio/paastot.csv','r') as paastot:
                 readCSV = csv.reader(paastot, delimiter=',')
                 #country = input("from what country do you want info? ")
                 #inputyear = input("For what year do you want info? ")
                 #country = 'Finland'
                 #inputyear = '1961'
                 headers=[]
                 countries=[]
                 data=[]
                 #loop trough rows in file
                 for row in readCSV:
                     numOfLines = readCSV.line_num
                     #We dont need the fist 4 lines
                     #Line 5 is headers. We can find
                     if numOfLines == 5:
                         headers = row
                         #print(headers)
                         indexY = headers.index(inputyear)
                         year = row[indexY]
                         print(year)
                         data.append(year)
                     elif numOfLines > 5:
                         #add all countruNames to list
                        countries.append(row[0])
                        #find selected country and co2emissions from selected year
                        if row[0] == country :
                            chosenCountry = row[0]
                            data.append(chosenCountry)
                            print(country + " CO2 emissions in the year: " + inputyear)
                            emissions = row[indexY]
                            data.append(emissions)
                            return jsonify({'data': data})

if __name__ == '__main__':
    app.run()
