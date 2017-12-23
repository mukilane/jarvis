/**
 * Adapted from Google Cloud Pub/Sub Nodejs example
 */

'use strict';

const PubSub = require('@google-cloud/pubsub');
const pubsub = PubSub();
const Buffer = require('safe-buffer').Buffer;

/**
 * Publishes a message to a Cloud Pub/Sub Topic.
 *
 * @example
 * gcloud alpha functions call publish --data '{"topic":"[YOUR_TOPIC_NAME]","message":"Hello, world!", "attributes": {"key": "val"}}'
 *
 *   - Replace `[YOUR_TOPIC_NAME]` with your Cloud Pub/Sub topic name.
 *
 * @param {object} req Cloud Function request context.
 * @param {object} req.body The request body.
 * @param {string} req.body.topic Topic name on which to publish.
 * @param {string} req.body.message Message to publish.
 * @param {object} req.body.attributes Attributes to publish
 * @param {object} res Cloud Function response context.
 */
exports.publish = function publish (req, res) {
  if (!req.body.topic) {
    res.status(500).send(new Error('Topic not provided. Make sure you have a "topic" property in your request'));
    return;
  } else if (!req.body.message) {
    res.status(500).send(new Error('Message not provided. Make sure you have a "message" property in your request'));
    return;
  }

  console.log(`Publishing message to topic ${req.body.topic}`);

  // References an existing topic
  const topic = pubsub.topic(req.body.topic);
  const publisher = topic.publisher();

  const message = new Buffer(req.body.message);
  const attributes = req.body.attributes;


  // Publishes a message
  return publisher.publish(message, attributes)
    .then(() => res.status(200).send('Message published.'))
    .catch((err) => {
      console.error(err);
      res.status(500).send(err);
      return Promise.reject(err);
    });
};

/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {object} event The Cloud Functions event.
 * @param {object} event.data The Cloud Pub/Sub Message object.
 * @param {string} event.data.data The "data" property of the Cloud Pub/Sub Message.
 * @param {function} The callback function.
 */
exports.subscribe = function subscribe (event, callback) {
  const pubsubMessage = event.data;

  // We're just going to log the message to prove that it worked!
  console.log(Buffer.from(pubsubMessage.data, 'base64').toString());

  // Don't forget to call the callback!
  callback();
};