Data Labs Assignment
--------------------

#### Glare detection from image metadata

To detect whether an image has glare or not using computer vision on high resolution images is very computationaly expensive when you are dealing with thousands of images.
To overcome this, we can make use of the image metadata to determine the posibilty of it having glare or not.
The metadata contains:

- “lat”: a float between -90 to 90 that shows the latitude in which the image was taken
- “lon”: a float between -180 to 180 that shows the longitude in which the image was taken
- “epoch”: Linux epoch in second
- “orientation”: a float between -180 to 180 the east-ward orientation of car travel from true
north. 0 means north. 90 is east and -90 is west

#### About the API

The API is built on Django and uses pysolar to determine the sun's altitude and azimuthal angle. The algorithm takes in the payload through a POST request and determines the possibility of glare based on the following conditions:

1. Azimuthal difference between sun and the direction of the car travel (and hence the
direction of forward- facing camera) is less than 30 degrees AND
2. Altitude of the sun is less than 45 degrees.

The API expects the input to be in the following format and acceptable values for the fields:

```
{
	“lat”: 49.2699648,
	“lon”: -123.1290368,
	“epoch”: 1588704959.321,
	“orientation”: -10.2,
}
```

###### Acceptable values:

- “lat”: a float between -90 to 90 
- “lon”: a float between -180 to 180
- “epoch”: Linux epoch in second
- “orientation”: a float between -180 to 180 

###### Response structure:

```{
	"glare": true,
	"status": 0,
	"request_id": 23
}
```

- glare: True or False depending on the input values. If null there was a problem with payload.
- status: ```0: ok```, ```1: Invalid lat```, ```2: Invalid lon```, ```3: Invalid orientation```.
- request_id: Each request is saved in the default sqllite database. This id represents the request number.


#### Prerequsits to run the API:
[Docker](https://www.docker.com/products/docker-desktop)

#### Steps to run the API:

1. Go to the root directory of the unzipped folder.

2. From the root directory use the following command in CLI: ```sudo docker-compose build```

3. Once the above step has been processed use: ```sudo docker-compose up```

4. In your choice of browser go to the following address: <http://0.0.0.0:8000/api/v1/sun_glare_algo/predict>

5. Enter the JSON input data and click _POST_

**The source code of the algorithm is present in** ```backend/server/apps/sg/sun_glare_algo/sun_glare.py```


#### References:
1. [Django RESTful Web Services](https://learning.oreilly.com/library/view/django-restful-web/9781788833929/)
2. [A novel method for predicting and mapping the presence of sun glare using Google Street View](https://arxiv.org/pdf/1808.04436.pdf)
3. [Deploy Machine Learning Models with Django](https://www.deploymachinelearning.com/#introduction)



