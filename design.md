Designed to be just as complicated as it needs to be. Instead 
of complicated models, the bare dictionaries are passed 
from the api up the chain.

Request methods are available to the user for extension or 
low level usage if need be, then those same methods were 
implemented for the movies endpoints.

I made a point to support multiple methods of secret store 
since the bearer token isn't likely to change.

Any of the three endpoints can be paginated with an optional argument 
if the user doesn't need the entire data set in memory at a time. 
Rate limiting is a concern if running multiple times to test 
the pagination, so a future improvement would probably address that.