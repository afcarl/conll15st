"""Sample Discourse Parser ready for evaluation on TIRA evaluation system

The parse should take three arguments

	$inputDataset = the folder of the dataset to parse.
		The folder structure is the same as in the tar file
		$inputDataset/pdtb-parses.json
		$inputDataset/pdtb-data.json
		$inputDataset/raw/...
		$inputDataset/conll_format/...

	$inputRun = the folder that contains the model file or other resources

	$outputDir = the folder that the parser will output 'output.json' to

"""
import json
import sys

class DiscourseParser(object):

	def __init__(self):
		pass

	def parse_file(self, input_file):
		documents = json.loads(open(input_file).read())	
		relations = []
		for doc_id in documents:
			relations.extend(self.parse_doc(documents[doc_id], doc_id))
		return relations

	def parse_doc(self, doc, doc_id):
		output = []
		num_sentences = len(doc['sentences'])
		token_id = 0
		for i in range(num_sentences-1):
			sentence1 = doc['sentences'][i]
			len_sentence1 = len(sentence1['words'])
			token_id += len_sentence1
			sentence2 = doc['sentences'][i+1]
			len_sentence2 = len(sentence2['words'])
			
			relation = {}
			relation['DocID'] = doc_id
			relation['Arg1'] = {}
			relation['Arg1']['TokenList'] = range((token_id - len_sentence1), token_id - 1)
			relation['Arg2'] = {}
			relation['Arg2']['TokenList'] = range(token_id, (token_id + len_sentence2) - 1)
			relation['Type'] = 'Implicit'
			relation['Sense'] = ['Expansion.Conjunction']
			relation['Connective'] = {}
			relation['Connective']['TokenList'] = []
			output.append(relation)
		return output

	def parse_sup(self, partial_relation_file):
		relations = []
		for x in open(partial_relation_file):
			relation = json.loads(x)
			if relation['Type'] == 'Implicit':
				relation['Sense'] = ['Expansion.Conjunction']
			elif relation['Type'] == 'Explicit':
				relation['Sense'] = ['Comparison.Contrast']
			else:
				relation['Sense'] = ['EntRel']
			relations.append(relation)
		return relations


if __name__ == '__main__':
	input_dataset = sys.argv[1]
	input_run = sys.argv[2]
	output_dir = sys.argv[3]
	parser = DiscourseParser()
	# Just to check that the parses are available
	_ = parser.parse_file('%s/pdtb-parses.json' % input_dataset)
	# actual relations
	relations = parser.parse_sup('%s/pdtb-data.json' % input_dataset)
	output = open('%s/output.json' % output_dir, 'w')
	for relation in relations:
		output.write('%s\n' % json.dumps(relation))
	output.close()

