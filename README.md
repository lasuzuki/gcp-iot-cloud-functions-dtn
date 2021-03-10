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

## The DTN Network 
The two node network is created following [this tutorial](https://github.com/lasuzuki/dtn-gcp-2nodes). The GCP Compute engine are located in two separate regions: 'us-central1' and 'europe-west-3'.