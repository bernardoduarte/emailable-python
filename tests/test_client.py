import pytest
import emailable

@pytest.fixture
def valid_client():
  return emailable.Client('test_7aff7fc0142c65f86a00')

@pytest.fixture
def valid_response(valid_client):
  return valid_client.verify('johndoe+tag@emailable.com')

  # def setUp(self):
  #   self.client = emailable.Client('test_7aff7fc0142c65f86a00')
  #   self.response = self.client.verify('johndoe+tag@emailable.com')

def test_invalid_api_key():
  client = emailable.Client('test_7aff7fc0141c65f86a00')
  with pytest.raises(emailable.AuthError):
    client.verify('evan@emailable.com')

def test_missing_api_key(valid_client):
  valid_client.api_key = None
  with pytest.raises(emailable.AuthError):
    valid_client.verify('evan@emailable.com')

def test_verify_returns_response(valid_response):
  assert isinstance(valid_response, emailable.Response)

def test_verification_role(valid_client):
  response = valid_client.verify('role@example.com')
  assert response.role

def test_verification_deliverable(valid_client):
  response = valid_client.verify('deliverable@example.com')
  assert response.state == 'deliverable'

def test_verification_tag(valid_response):
  assert valid_response.tag == 'tag'

def test_verification_name_and_gender(valid_response):
  # name and gender checks only get run for certain verification states
  if valid_response.state in ['deliverable', 'risky', 'unknown']:
    assert valid_response.first_name == 'John'
    assert valid_response.last_name == 'Doe'
    assert valid_response.full_name == 'John Doe'
    assert valid_response.gender == 'male'
  else:
    assert valid_response.first_name is None
    assert valid_response.last_name is None
    assert valid_response.full_name is None
    assert valid_response.gender is None

def test_batch_creation(valid_client):
  response = valid_client.batch(
    ['evan@emailable.com', 'jarrett@emailable.com']
  )
  assert response.id is not None

def test_batch_status(valid_client):
  response = valid_client.batch_status('5cff27400000000000000000')
  assert response.emails is not None
  assert response.id is not None
  assert response.reason_counts is not None
  assert response.total_counts is not None

def test_account(valid_client):
  response = valid_client.account()
  assert response.owner_email is not None
  assert response.available_credits is not None
