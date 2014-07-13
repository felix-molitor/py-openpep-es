from flask import Flask

import os
import csv
import logging
from flask import Flask, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename

from elasticsearch import Elasticsearch
from elasticsearch import helpers

from forms import PEPForm
from es_setup import es, INDEX, DOC_TYPE
from readers import read_csv


UPLOAD_FOLDER = '/tmp/pep/uploads'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # max 16MB


ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def bulk_create(objs):
	actions = []
	for obj in objs:
	    action = {
	        "_index": INDEX,
	        "_type": DOC_TYPE,
	        "_source": obj
        }
	    actions.append(action)

	helpers.bulk(es, actions)


@app.route('/', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
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
			return render_template('upload_success.html')
		else:
			# could render invalid_pep_forms.errors
			return render_template('upload_error.html')
	    # if all valid pass on to elasticsearch backend
	    # ...
	else:
		# just a mock handler to display the file upload form
	    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)