from pysolar.solar import *
import datetime
import pytz
import json
import pandas as pd

class SunGlareAlgorithm():
  def check_data(self,input_data):
    if input_data['lat'].iloc[0] < -90 or input_data['lat'].iloc[0] > 90:
      return {"status": 1}
    if input_data['lon'].iloc[0] < -180 or input_data['lon'].iloc[0] > 180:
      return {"status": 2}
    if input_data['orientation'].iloc[0] < -180 or input_data['orientation'].iloc[0] > 180:
      return {"status": 3}
    return {"status": 0}

  def normalizeAngle(self, angle):
    while angle <= -180:
      angle += 360
    while angle > 180:
      angle -= 360
    return angle

  def predict(self,input_data):
    input_data = pd.DataFrame(input_data, index=[0])
    response = self.check_data(input_data)
    glare = None
    if response['status'] == 0:
      date =datetime.datetime.fromtimestamp(input_data['epoch'].iloc[0],pytz.UTC)
      alt = get_altitude(input_data['lat'].iloc[0],input_data['lon'].iloc[0],date)
      az = get_azimuth(input_data['lat'].iloc[0],input_data['lon'].iloc[0],date)
      normalized_az = self.normalizeAngle(az)
      if abs(abs(normalized_az) - abs(input_data['orientation'].iloc[0])) < 30 and (alt < 45 and alt > 0):
        glare = True
      else:
        glare = False
    return {"glare": glare, "status": response['status']}



