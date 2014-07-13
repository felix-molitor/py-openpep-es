import csv

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

