from flask import Flask, render_template, request
import base64, json
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/render/<base64encodedjson>')
def render(base64encodedjson):
    decodedString = base64.b64decode(base64encodedjson).decode('utf-8')
    print(decodedString);
    return generate_gantt(decodedString)


def generate_gantt(decodedString):
  data = json.loads(decodedString);
  page_title = data['title']
  table_string = ""
  graph_string = ""
  for item in data['items']:
    id = item['key']

    duration = item['duration']
    percent_complete = 0
    start_date = "null"
    if item['start_date']:
      start_date = """new Date("%s")""" % (item['start_date'])

    dependencies = "\'" + item['dependencies'] + "\'"
    if dependencies == "":
      dependencies = "null"
    resource = item['resource']
    # task id, task name, resource, start date, end date, duration, percent_complete dependencies
    graph_item = """['%s', '%s', '%s', %s, null, daysToMilliseconds(%s), %s, %s],""" % (id, item['title'], resource, start_date, duration, percent_complete, dependencies)
    graph_string = graph_string + graph_item + '\n'

    # if not item['duplicate']:
    if True:
      list_item = """<tr><th scope="row"><span id="%s">%s</span></th><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (id, item['key'], item['title'], str(item['description']), dependencies, str(duration), resource)
      table_string = table_string + list_item + '\n'


  graph_string = graph_string.rstrip(",\n")
  graph_height = 45 + 42 * len(data['items'])
  graph_height = "\"" + str(graph_height) + "\""
  html = """<html>
    <head>
      <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans" />
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
      <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
      <script type="text/javascript">
        google.charts.load('current', {'packages':['gantt']});
        google.charts.setOnLoadCallback(drawChart);
     
        window.onload = drawChart;
        window.onresize = drawChart;
     
        function daysToMilliseconds(days) {
          return days * 24 * 60 * 60 * 1000;
        }
     
        function drawChart() {
     
          var data = new google.visualization.DataTable();
          data.addColumn('string', 'Task ID');
          data.addColumn('string', 'Task Name');
          data.addColumn('string', 'Resource');
          data.addColumn('date', 'Start Date');
          data.addColumn('date', 'End Date');
          data.addColumn('number', 'Duration');
          data.addColumn('number', 'Percent Complete');
          data.addColumn('string', 'Dependencies');
     
          data.addRows([
    """ + graph_string + """
          ]);
     
          var options = {
            title: 'Harvest Project Plan',
            height: """ + graph_height + """,
            gantt: {
              criticalPathEnabled: true,
              criticalPathStyle: {
                stroke: '#e64a19',
                strokeWidth: 5
              },
              labelStyle: {
                fontName: 'Open Sans',
                fontSize: 14,
                color: '#757575'
              },
            }
          };
     
          var chart = new google.visualization.Gantt(document.getElementById('chart'));
     
          chart.draw(data, options);
        }
      </script>
      <style>
        body {
          font-family: 'Open Sans' !important;
          background: url(groovepaper.png);
        }
     
        text {
          font-family: 'Open Sans' !important
        }
     
        .center {
          margin: auto;
          width: 75%;
          padding: 10px;
        }
     
        #header {
          padding-top: 20px;
          text-align: center;
          padding-bottom: 20px;
        }
     
        #chart {
          border-radius: 5px;
          box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
          background-color: white
        }
     
        #table {
          padding-top: 60px;
        }
      </style>
    </head>
    <body>
      <div class="center" id="header">
        <h1>""" + page_title + """</h1>
      </div>
      <div class="center" id="chart"></div>
      <div class="center" id="table">
        <table class="table">
          <thead class="thead-dark">
            <tr>
              <th scope="col">Key</th>
              <th scope="col">Title</th>
              <th scope="col">Description</th>
              <th scope="col">Dependencies</th>
              <th scope="col">Duration in Days</th>
              <th scope="col">Resource</th>
            </tr>
          </thead>
          <tbody>
    """ + table_string + """
          </tbody>
        </table>
      </div>
    </body>
    </html>"""
  return html
