from flask import Flask

import os
import csv
import logging
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

from elasticsearch import Elasticsearch
from elasticsearch import helpers

from forms import PEPForm
from es_setup import es, INDEX, DOC_TYPE

UPLOAD_FOLDER = '/tmp/pep/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # max 16MB


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class DictObj ( dict ):
  "A wrapper for dictionaries that feel like py objects"
  def __getattr__(self, key):
    if key in self:
      return self[key]
    else:
      try:
        return super(DictObj, self).__getattr__(key)
      except:
        pass
    return None


def read_csv(inf, close_file=True):
	'Reads a csv file in as a list of objects'
	def from_csv_line(l, h):
		return DictObj(dict(zip(h, l)))		
	iter = csv.reader(inf).__iter__()
	header = map(lambda x: x.strip(), iter.next())
	for i in iter:
		yield from_csv_line(i, header) 
	if close_file:
		inf.close()


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as csvfile:
			peps = read_csv(csvfile)
			validated_peps = []
			invalid_pep_forms = []
			for pep in peps:
				print ">>>", pep
				form = PEPForm(None, obj=pep)
				if form.validate():
					validated_peps.append(form.data)
				else:
					invalid_pep_forms.append(form)
	if validated_peps and not invalid_pep_forms:		
		bulk_create(validated_peps)
	print 'VALID', validated_peps
	for inv_pep in invalid_pep_forms:
		print 'INVALID'
		print invalid_pep_forms.errors
    # if all valid pass on to elasticsearch backend
    # ...
	return "uploaded!"


def bulk_create(objs):
#	j = 0
	actions = []
	for obj in objs:
	    action = {
	        "_index": INDEX,
	        "_type": DOC_TYPE, #	        "_id": j,
	        "_source": obj
        }
	    actions.append(action)
	    # j += 1

	helpers.bulk(es, actions)


# just a mock handler to display the file upload form
@app.route("/", methods=['GET'])
def hello():
    return '''
    <!doctype html>
    <title>Upload new Open PEP File</title>
    <h1>Upload new File</h1>
    <form action="/upload" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
