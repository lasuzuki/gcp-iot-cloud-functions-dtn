# Controlling Raspberry Pi on Google Cloud with Cloud Functions via DTN :rocket:
This project has been developed by Dr Lara Suzuki :woman_technologist: [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/larasuzuki.svg?style=social&label=Follow%20%40larasuzuki)](https://twitter.com/larasuzuki) and supervised by Vint Cerf :technologist: [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/vgcerf.svg?style=social&label=Follow%20%40vgcerf)](https://twitter.com/vgcerf), both at Google Inc.

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/lasuzuki/StrapDown.js/graphs/commit-activity)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
![Profile views](https://gpvc.arturio.dev/lasuzuki)
[![GitHub contributors](https://img.shields.io/github/contributors/Naereen/StrapDown.js.svg)](https://GitHub.com/lasuzuki/StrapDown.js/graphs/contributors/)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/lasuzuki)

[![ForTheBadge built-with-science](http://ForTheBadge.com/images/badges/built-with-science.svg)](https://GitHub.com/lasuzuki/)

In this tutorial I will demonstrate how to connect a Raspberry Pi and Sensor Hat onto Google Cloud using cloud Pub/Sub, and get the data persisted in Big Query. I will then on demonstrate how to create a cloud function to talk to IOT Core and send commands to the Raspberry Pi. The commands to the Raspberry Pi is sent over DTN.

# Introduction
Please find an introduction to Pub/Sub with Raspberry Pi in [this repo](https://github.com/lasuzuki/dtn-gcp-iot). An introduction to Sense Hat can be found in [this repo](https://github.com/lasuzuki/gcp-iot-bigquery). Please do get familiar with those as we will build on them to create our project.

# The DTN Network 
The two node network is created following [this tutorial](https://github.com/lasuzuki/dtn-gcp-2nodes). The GCP Compute engine are located in two separate regions: **us-central1** and **europe-west-3**. Once you set up the two nodes in the two Compute Engines you are ready to move to the next session.

# The Raspberry Pi and Sense Hat 
The Raspberry PI and the Sense Hat are assembled following [this tutorial](https://github.com/lasuzuki/dtn-gcp-iot). Once you get it running and publishing message to the Google Cloud Pub/Sub you are ready to proceed to the next step.

## The sensing capabilities of Sense Hat

The schematics of the Raspbery Pi Sense Hat can be found [here](https://www.raspberrypi.org/documentation/hardware/sense-hat/images/Sense-HAT-V1_0.pdf) and it is illustrated in the image below.

<img src="https://github.com/lasuzuki/gcp-iot-bigquery/blob/main/blob/rotation_movement.png" width=400 align=center>

The Sense HAT is an add-on board for Raspberry Pi comprising of a 8×8 RGB LED matrix, a five-button joystick and the following sensors: Gyroscope, Accelerometer, Magnetometer, Temperature, Barometric pressure and Humidity.

The shift register driving the LED Matrix is a LED2472G connected via an Atmel ATTINY88 communicating via i2c at address 0x46 with the Pi. The Multi-Directional SKRHABE010 Switch/Joystick is similarly controlled.

The sensors themselves also operate over the i2c bus:

- The IMU (Accelerometer and Magnetometer) through a LSM9DS1 found at i2c address 0x1c(0x1e) and 0x6a(0x6b), with Interrupts on the ATTINY88.

- Environmental sensors are represented by a LPS25H Pressure/Temperature sensor at address 0x5c and by a HTS221 Humidity/Temperature sensor at 0x5f on the i2c bus.

<img src="https://github.com/lasuzuki/gcp-iot-bigquery/blob/main/blob/rotation_movement.png" width=400 align=center>

## The code for your Raspberry Pi
In your Raspberry Pi run the code **iot.py** (Adapted from Gaby Weiss), and change the variables accordingly:

```python
ssl_private_key_filepath = 'location_of_demo_private.pem'
ssl_algorithm = 'RS256' 
root_cert_filepath = 'location_of_roots.pem'
project_id = 'project_id'
gcp_location = 'region'
registry_id = 'registry_id'
device_id = 'your_device_id'
```  

# Controlling your Raspberry Pi using Google Cloud Functions

Cloud Functions allow us to develop faster by writing and running small code snippets that respond to events. We can just write your code and let Google Cloud handle the operational infrastructure.  

In our example we will be using Cloud functions to talk back to our Raspberry Pi given a change in the environment sensors. Below are the steps to use Google Cloud Functions:

1. In the Google Cloud Console search bar, type Cloud Functions
2. In the Cloud Functions interface, at the top of the page click on **Create Functions**
3. In the new interface, under **Basics**, give it a *Function Name* and a *Region*
4. Under **Trigger**, leave HHTP selected. In the Authentication section, select **Require Authentication**. You will be prompted to select which service account to use. Select the service account that has *Cloud Functions Admin* associated with it.
5. Hit **Save**
6. At the bottom of the screen hit **Next**

Here is where our code will be introduced to send a message to Raspberry Pi. Follow the steps below:
1. In the **Runtime** select box, pick *Puthon 3.7*
2. In the **Source Code** section, select *requirements.txt* and insert the following dependencies

```python
google-cloud-iot
google-cloud
```
3. Now select *main.py*. Here is where the code **main.py** will go. 
4. On **Entry point** add Entry point to your code, e.g. the exported function name, in our case, *sense_hat*
5. Hit **Deploy**
6. After a few minutes, if nothing went wrong, you will see your Cloud Function successfully deployed.
7. Execute the code **iot.py** in your Raspberry Pi so that it can receive instructions from Cloud Function
8. Click on the function deployed
9. On the Trigger tab, open the URL and append at the end *?message=blue*
10. If all is correct, your Sense Hat should be turned blue

 # The Subscription Code for Host1 - Goldstone
 In your Host1 and Host2, you will have Pub/Sub set up as per this [tutorial](https://github.com/lasuzuki/dtn-gcp-iot). Now you will introduce a few changes to the code base. After starting the code **iot.py** in the Raspberry Pi:

# Host1 Configuration
Use the same configuration as in the [IOT on GCP tutorial](https://github.com/lasuzuki/dtn-gcp-iot)After starting ION, execute the code **host1_iot.py**. This code will
1. Listen for sensing data arriving at the **Pub/Sub** Topic
2. Will persist the telemetry data on **BigQuery** 
3. Will save on a file the telemetry data
4. Will send the saved telemetry data to **Host2** via DTN using *bpsendfile*

# Host2 Configuration
Use the same configuration as in the [IOT on GCP tutorial](https://github.com/lasuzuki/dtn-gcp-iot)After starting ION, execute the code **host2_iot.py**. This code will
1. Listen for the arrival of a telemetry file via DTN (bprcv)
2. Will extract the measure values from the json file
