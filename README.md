### Installation:

pip install the_one_api_sdk_swilson

### Usage:

#### Auth
Supports basic auth with the-one-api.dev to gather the token or
the api client auth method can be called directly with a known token

Account needs to be created at https://the-one-api.dev/sign-up

Calling the constructor with username and password will gather and set the token for you

`api = ApiClient(username='user', password='pass') `

#### Parameters
The api supports pagination, filtering, and sorting parameters. 
These are passed as an optional dict to any of the request methods.
Filtering parameters can be used on any of field in the document.

Filtering params that include special characters ('<', '>', etc) need
to have the entire param set as the key and an empty string as the value

`{'budgetInMillions>1000': ''}`

Pagination is built-in. Beware of rate limiting if using small page sizes