from eval_string import get_value


def make_row_float(row):
	vals = []
	for s in row:
		v = get_value(s, op=float, vdefault=None)
		vals.append(v)
	return vals
