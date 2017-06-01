from ga4gh.client import client
from collections import Counter
import json


##### Global Constants
filename = ""

# Missing from MT
# - Variant Names

if __name__ == '__main__':

	# [1] Boilerplate code to initialize GA4GH client
	c = client.HttpClient("http://1kgenomes.ga4gh.org")
	dataset = c.search_datasets().next()

	# [2] Fetch variant set
	for variant_set in c.search_variant_sets(dataset_id=dataset.id):
		if variant_set.name == "phase3-release":
			var_set = variant_set

	# [3] Iterate through variants, performing successive filtering
	# 	 i. VCF is first run through Haplogrep
	#	 ii. Haplogrep returns path down Phylotree
	#	 iii. Look at the Phylotree path. Starting at the variant closest to
	#		  root level look at the position number. In positions.txt write
	#		  the position number down. Continue doing this for each variant
	#		  down the path, writing each position number on a new line.
	# Lily Mendel Example:
	# Phylotree Path: [H, H2, H2a, H2a2, H2a2a, H2a2a1]
	# Positions: [6776, 1438, 4769, 750, 8860, 263]
	# variant_starts = [6776, 1438, 4769, 750, 8860, 263]
	with open('positions.txt', 'r') as f:
		variant_starts = [int(x) for x in f.read().split('\n')]
	# print(variant_starts)
	variant_map = {} # Maps variant position to GA server ID
	for variant in c.search_variants(variant_set_id=var_set.id, reference_name='MT'):
		if variant.start  in variant_starts:
			print(variant.start)
			variant_map[int(variant.start)] = str(variant.id)
		if variant.end in variant_starts:
			print(variant.end)
			variant_map[int(variant.end)] = str(variant.id)
	
	# [4] Build set containing all call set ids
	id_set = set()
	for call_set in c.search_call_sets(variant_set_id=var_set.id):
		id_set.add(call_set.id)

	# [5] For each variant in the phylotree path, perform an iterative filter
	for key in variant_starts:
		if key in variant_map.keys():
			current = set()
			variant = c.get_variant(variant_id=variant_map[key])
			for call in variant.calls:
				if call.genotype.values[0].number_value == 1 and call.call_set_id in id_set:
					current.add(call.call_set_id)
			if len(current) == 0:
				break
			print(len(id_set))
			id_set = current
	
	# [6] Display nearest relatives
	id_list = [str(x) for x in list(id_set)]
	names = set()
	for x in id_list:
		call_set = c.get_call_set(call_set_id=x)
		names.add(call_set.name)
	
	# Get descriptions of closest individuals
	descriptions = []
	for individual in c.search_individuals(dataset_id=dataset.id):
		if individual.name in names:
			descriptions.append(str(individual.description))

	region_map = {}
	regions = Counter()
	genders = Counter()
	for description in descriptions:
		region, desc, gender = description.split(' - ')
		if region not in region_map.keys():
			region_map[region] = desc
		regions[region] += 1
		genders[gender] += 1

	print('Region of closest relatives')
	for region, count in regions.most_common():
		print("{} - {}: {}".format(region, region_map[region], count))
	print('Gender of closest relatives')
	for gender, count in genders.most_common():
		print("{}: {}".format(gender, count))

	data = {'regions': regions, 'genders': genders}
	filename = 'data.json'
	with open(filename, 'w') as f:
		json.dump(data, f, indent=4)
	





