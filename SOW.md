# Rule Engine REST API

## Abstract

Given many remotely installed temperature sensors, write an API that will allow users to create simple rules (temperature greater than {x}, temperature less than {x}, temperature between {x} and {y}) that will send an sms alert to the requested phone number. Please work out of a publicly-visible github repository and include a readme with any instructions require to run the API locally. Any language/db preferences are completely up to you.

## Data

An incoming point will assume the JSON data format:
```
{
	id: {GUID},
	value: {temperature value}
	unit: [“fahrenheit” | “celsius”]
}
```

These points can be assumed to be POSTed to an endpoint in the API with the above format.

## Rules

Rules should be able to be created and read. A user must be able to specify which sensor they want the rule to act on (point’s id), the trigger point for the temperature value, and what type of comparison logic to use (> than, < than, > and <). A rule must be able to account for either celsius or fahrenheit points. However assume rules to be set up using celsius for the value. The format for storing these rules and how they are stored is up to you.

## Processing Rules

Alerts should be sent immediately after the condition for a rule are met by a point’s data

## In Scope

- Create and Read rules
- Trigger when temperature is more than {X}
- Trigger when temperature is less than {X}
- Trigger when temperature is more than or less than {X}
- API endpoint that will receive temperature data in the above format
- Processing rules live on incoming point data
- Sending an sms alert (twilio) when a rule should be executed
- Dockerfile and docker-compose for running the api/database

## Not in Scope

- Auth/dns/CI/CD
- Anything related to users
- Storing points or their IDs as metadata
- Any automation around pushing points to the API
- Rules that act on more than one unique point
- Any front-end at all
- Security
- Updating or Deleting rules
- Searching or filtering rules

Best practices should be followed
