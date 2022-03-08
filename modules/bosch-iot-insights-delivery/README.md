
Receive data from MQTT and publish to Insights.

# Prerequisites

Create a `.env` file and add at least the following environment variables:

```dotenv
MQTT_USERNAME=mqtt user
MQTT_PASSWORD=mqtt passowrd

INSIGHTS_USER=insights api user
INSIGHTS_API_KEY=insights api key
```

Find additional environment variables in [`index.js`](./index.js).

# Running

```shell
# install dependencies
yarn install
# running
yarn start
```
