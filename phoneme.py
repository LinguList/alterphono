# encoding: utf-8

class Phoneme:
	def __init__(self, features=[]):
		self.features = []

		# set each feature, if possible
		for feature in features:
			self.set_feature(feature)

	# set a binary or articulatory feature, if possible
	def set_feature(feature):
		# assume that binary features will always begin with '+' or '-'
		if feature[0] in '+-':
			pass
		else:
			# get the feature category
			pass
			
	def show(self):
		print self.features

p = Phoneme()
p.show()
