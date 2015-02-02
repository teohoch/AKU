def to_dictionary(list):
	dict = {}
	for element in list:
		dict[element[0]] = element[1]
	return dict

def select_field_transform(data):
	fixed = []
	for k in data:
		d = str(k[1])
		fixed.append([d,d])
	return fixed