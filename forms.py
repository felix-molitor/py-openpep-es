from wtforms import Form
from wtforms import TextField, IntegerField, validators
from wtforms.validators import DataRequired, Length

class PEPForm(Form):
	Citizenship = TextField('Citizenship', [DataRequired()])
	FirstName = TextField('FirstName', [DataRequired()])
	LastName = TextField('LastName', [DataRequired()])
	Source = IntegerField('Source', [DataRequired()]) # int

	Website = TextField('Website')
	Register  = TextField('Register')
	Subcategory = TextField('Subcategory')
	Title = TextField('Title')
	Category = TextField('Category')
	MiddleName = TextField('MiddleName')
	Ministery = TextField('Ministery')
	Position = TextField('Position')
	MonthlyIncome = TextField('MonthlyIncome')
	Currency = TextField('Currency')
	Residence  = TextField('Residence')
# 	  uuid = TextField('uuid', [validators.Length(min=4, max=25)]) # backend generated
