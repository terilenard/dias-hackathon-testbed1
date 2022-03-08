/*****************************************************************************
 * Copyright (c) 2022 Bosch.IO GmbH
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 *
 * SPDX-License-Identifier: MPL-2.0
 ****************************************************************************/

import {connect} from 'mqtt';
import needle from 'needle';
import HttpsProxyAgent from 'https-proxy-agent';
import HttpProxyAgent from 'http-proxy-agent';


const mqttConfig = {
  username: process.env.MQTT_USERNAME ?? null,
  password: process.env.MQTT_PASSWORD ?? null,
  protocol: process.env.MQTT_PROTOCOL ?? 'mqtt',
  host: process.env.MQTT_HOST ?? '127.0.0.1',
  port: Number.parseInt(process.env.MQTT_PORT ?? '1883'),
  topic: process.env.MQTT_TOPIC ?? 'telemetry',
};

const insightsConfig = {
  user: process.env.INSIGHTS_USER ?? null,
  apiKey: process.env.INSIGHTS_API_KEY ?? null,
  url: process.env.INSIGHTS_URL ?? 'https://bosch-iot-insights.com/data-recorder-service/v2/',
  collection: process.env.INSIGHTS_COLLECTION ?? 'testbed_1',
  project: process.env.INSIGHTS_PROJECT ?? 'Testbed-1',
  type: process.env.INSIGHTS_METADATA_TYPE ?? 'testbed1',
};

const httpsProxyAgent = process.env.HTTPS_PROXY ? new HttpsProxyAgent(process.env.HTTPS_PROXY) : null;
const httpProxyAgent = process.env.HTTP_PROXY ? new HttpProxyAgent(process.env.HTTP_PROXY) : null;

class MqttListener {
  constructor(config) {
    this._config = config;
  }

  connect(listener) {
    console.log(`Connecting to MQTT broker with config: ${JSON.stringify(mqttConfig)}`);
    this._client = connect(`${this._config.protocol}://${this._config.host}:${this._config.port}`,
      {
        username: this._config.username,
        password: this._config.password,
      },
    );
    this._client.on('connect', this._onConnected.bind(this));
    this._client.on('message', (topic, message) => this._onMessage(listener, topic, message));
  }

  _onConnected() {
    console.log(`Connected to MQTT broker`);
    this._client.subscribe(this._config.topic, (err) => {
      if (err) {
        console.log(`Error while subscribing to topic ${this._config.topic}: ${err}`);
        this._onConnected();
      } else {
        console.log(`Subscribed to topic ${this._config.topic}`);
      }
    });
  }

  _onMessage(listener, topic, message) {
    console.log(`Received message on topic ${topic}: ${message}`);
    const json = this._tryParseToJson(message);
    if (json !== null) {
      listener(json);
    }
  }

  _tryParseToJson(string) {
    try {
      return JSON.parse(string);
    } catch (e) {
      console.log(`Error while parsing <${string}> to JSON: ${e}`);
    }
    return null;
  }
}

class InsightsDataRecorder {

  constructor(config) {
    this.dataRecorderUrl = `${config.url}${config.project}`;
    this.basicAuth = Buffer.from(`${config.user}:${config.apiKey}`).toString('base64');

    this.options = {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Basic ${this.basicAuth}`,
        'X-Metadata': `type=${config.type};dataType=String`,
      },
      json: true,
    };

    console.log(`Default options for Insights: ${JSON.stringify(this.options)}`);
    if (process.env.HTTPS_PROXY && this.dataRecorderUrl.startsWith('https://')) {
      this.options.agent = httpsProxyAgent;
    }

    if (process.env.HTTP_PROXY && this.dataRecorderUrl.startsWith('http://')) {
      this.options.agent = httpProxyAgent;
    }
  }

  publish(data) {
    try {
      console.log(`Sending next message to Insights at URL: ${this.dataRecorderUrl}`);
      needle('POST', this.dataRecorderUrl, JSON.stringify(data), this.options)
        .then(response => {
          if (response.statusCode >= 400) {
            throw new Error(`Error response with status ${response.statusCode}: ${JSON.stringify(response.body)}`);
          }
          return response.body;
        })
        .then((response) => {
          console.log(`Successfully published data to Insights: ${JSON.stringify(response)}`);
        }).catch((error) => {
        console.log(`Error while sending data ${data} to insights: ${error}`);
      });
    } catch (error) {
      console.log(`Error while sending data ${data} to insights: ${error}`);
    }
  }

}

const insightsDataRecorder = new InsightsDataRecorder(insightsConfig);
const mqttListener = new MqttListener(mqttConfig);

mqttListener.connect(data => insightsDataRecorder.publish(data));

// run forever
setInterval(() => {
}, 1 << 30);
