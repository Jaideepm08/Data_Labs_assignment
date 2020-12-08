# to be implemented

import pandas as pd

class SunGlareAlgorithm:

	def __init__(self,input_data):
		self.input_data = pd.DataFrame(input_data, index=[0])

	def predict(self):
		if (self.input_data['lat'].values < 0).any():
			return {"prediction":True,"status":"ok"}
		else:
			return {"prediction":False,"status":"ok"}
		
