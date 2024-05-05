from flask import Flask, request, jsonify, render_template

from xata.client import XataClient


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    #return a template file
    name = 'peekay'
    return render_template('index.html', name=name)


@app.route('/data', methods=['POST'])
def data():
    # get name from input
    name = request.form['name']
    print(name)
    xata = XataClient()
    data = xata.data().search_branch({
        "query": name,
        "tables": [
            {
                "table": "tag",
                "target": [
                    {
                        "column": "name"

                        }
                    ]
                },
            {
                "table": "image",
                "target": []
                },
            {
                "table": "tag-to-image",
                "target": []
                },
            {
                "table": "users",
                "target": [
                    {
                        "column": "names",
                        "weight": 10
                        },
                    {
                        "column": "xata.createdAt"
                        },
                    {
                        "column": "xata.updatedAt"
                        }
                    ],
                "boosters": [
                    {
                        "valueBooster": {
                            "value": "",
                            "column": "names",
                            "factor": 10
                            }
                        }
                    ]
                }
            ],
        "fuzziness": 2,
        "prefix": "phrase"
        })
    print(data);
    records = data['records']


    # for record in records:
    #     record_id = record['id']
    #     record_name = record['names']
        # record_xata_data = record['xata']

        # print("Record ID: ", record_id)
        # print("Record Name: ", record_name)
        # print("Xata Data: ", record_xata_data, "\n")
    # return a an list of records
    return render_template('data.html', records=records)



if __name__ == '__main__':
    app.run(debug=True)


