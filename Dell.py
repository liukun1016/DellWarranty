import requests
import yaml
import itertools

config_path = "/Users/kunliu/Desktop/work/dell_config.yml"

with open(config_path, 'r') as input:
	config = yaml.load(input)

def svctags_random(per, d, suffix):
	"""
	Generate cartisen product of per, say per="ABC", d=3 then
	AAA, AAB, AAC, ABA, ABB, ABC, ACA...
	If suffix specified, then add it to each result above.
	"""
	result_T = itertools.product(per ,repeat=d)
	result_L = []
	for r_T in result_T:
		result_L.append(''.join(r_T) + suffix)
	return result_L

def svctags_flatten(svctags_L):
	"""
	Given a list of service tags, return the concatenated string delimited by "|"
	"""
	if len(svctags_L) == 0:
		return ""
	elif len(svctags_L) == 1:
		return svctags_L[0]
	else:
		return "|".join(svctags_L)

def check_svctag_valid(svctag):
	web_url = "http://www.dell.com/support/home/cn/zh/cndhs1/product-support/servicetag/"+svctag
	resp_suffix = requests.get(web_url).url
	return True if str(resp_suffix).endswith(svctag) else False

def filter_invalid_svctags(svctags_L):
	valid_svc_L = []
	i = 0
	for svc in svctags_L:
		i+=1
		if check_svctag_valid(svc):
			print "~~~~~~~~~~~~~Valid tag:", svc, "remained=", str(i)
			valid_svc_L.append(svc)
	return valid_svc_L

def valid_svctags_batch(suffix, d=4, offset=100, per="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
	svctags_random_L = svctags_random(per, d, suffix)
	print "1. %s random service tags generated =====" % len(svctags_random_L)
	valid_svc_L = filter_invalid_svctags(svctags_random_L)
	print "2. %s invalid service tags filtered out -----" % (len(svctags_random_L) - len(valid_svc_L))
	temp_L = []
	turn = 1
	
	while turn * offset <= len(valid_svc_L):
		begin = (turn - 1) * offset
		end = turn * offset
		temp_L.append(valid_svc_L[begin:end])
		turn += 1
	if turn * offset > len(valid_svc_L):
		begin = (turn - 1) * offset
		temp_L.append(valid_svc_L[begin:])
	print "3. Put valid tags in a Temp List, %s in total ######" % len(temp_L)
	result_L = []
	for L in temp_L:
		result_L.append(svctags_flatten(L))
	print "4. Flatten valid tags as a List of List, %s in total ******" % len(result_L)
	
	return result_L

L = svctags_generator_batch("3JR32", d=2)

api_key=config['api_key']
data_format="json"
svctags_L=["3P3JR32", "G3VG2W1","DCVYWW1","GGVG2W1","GGGG2W1"]
api_url="https://api.dell.com/support/v2/assetinfo/warranty/tags.%s?svctags=%s&apikey=%s"
url = api_url % (data_format, svctags_L[0], api_key)

json_resp = requests.get(url).json()
dell_asset_array = json_resp['GetAssetWarrantyResponse']['GetAssetWarrantyResult']['Response']['DellAsset']