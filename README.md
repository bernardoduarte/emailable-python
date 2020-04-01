# Blaze Verify Python Library

[![Version](https://img.shields.io/pypi/v/blazeverify.svg)](https://pypi.org/project/blazeverify/)
[![Build Status](https://travis-ci.com/blazeverify/blazeverify-python.svg)](https://travis-ci.com/blazeverify/blazeverify-python)
[![Maintainability](https://api.codeclimate.com/v1/badges/dcb962c96795974051fc/maintainability)](https://codeclimate.com/github/blazeverify/blazeverify-python/maintainability)

This is the official python wrapper for the Blaze Verify API.

## Documentation

See the [Python API docs](https://blazeverify.com/docs/api#python).

## Installation

```shell
pip install blazeverify
```

## Usage

The library needs to be configured with your account's API key which is available in your [Blaze Verify Dashboard](https://app.blazeverify.com/api).

### Setup

```python
import blazeverify

client = blazeverify.Client('live_...')
```

### Verification

```python
# verify an email address
response = client.verify('evan@blazeverify.com')
response.state
=> 'deliverable'

# additional parameters are available. see API docs for additional info.
client.verify('evan@blazeverify.com', smtp=False, accept_all=True, timeout=25)
```

#### Slow Email Server Handling

Some email servers are slow to respond. As a result, the timeout may be reached
before we are able to complete the verification process. If this happens, the
verification will continue in the background on our servers. We recommend
sleeping for at least one second and trying your request again. Re-requesting
the same verification with the same options will not impact your credit
allocation within a 5 minute window.

A slow response will return with a 249 status code.

```python
response = client.verify('slow@example.com')
response.status_code
=> 249
response.message
=> 'Your request is taking longer than normal. Please send your request again.'
```

### Batch Verification

#### Start a batch

```python
emails = ['evan@blazeverify.com', 'support@blazeverify.com', ...]
response = client.batch(emails)
response.id
=> '5cff27400000000000000000'

# you can optionally pass in a callback url that we'll POST to when the
# batch is complete.
response = client.batch(emails, callback_url='https://blazeverify.com/')
```

#### Get the status / results of a batch

To get the status of a batch call `batch_status` with the batch's id. If your batch is still being processed, you will receive a message along with the current progress of the batch. When a batch is completed, you can access the results in the `emails` attribute.

```python
response = client.batch_status('5cff27400000000000000000')

# if your batch is still running
response.processed
=> 1
response.total
=> 2
response.message
=> 'Your batch is being processed.'

# if your batch is complete
response.emails
=> [{'email': 'evan@blazeverify.com', 'state': 'deliverable'...}, {'email': 'support@blazeverify.com', 'state': 'deliverable'...}...]

# get the counts
response.total_counts
=>{'deliverable': 2, 'undeliverable': 0 ...}
response.reason_counts
=>{'accepted_email': 2, 'rejected_email': 0 ...}
```

## Development

Tests can be run with the following command:

```shell
python setup test
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/blazeverify/blazeverify-python.
