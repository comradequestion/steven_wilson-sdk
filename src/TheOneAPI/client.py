from requests import Session
import logging


class ApiClient:
    """
    API client class
    """
    def __init__(self,
                 host: str = 'the-one-api.dev',
                 username: str = None,
                 password: str = None,
                 verify: bool = True):
        self.session = Session()
        self.host = host
        self.base_url = f"https://{host}"

        self.username = username
        self.password = password

        if not username or not password:
            logging.warning('Username and/or password not defined, use set_bearer_auth to specify auth token')
        else:
            self.set_bearer_auth(self.get_token())

        self.session.verify = verify

    def get_token(self) -> str:
        """
        Gets bearer token from host using member username and password variables
        """

        resp = self.session.post(
            self.build_url('/auth/login'),
            data={
                'email': self.username,
                'password': self.password
            }
        )

        if resp.ok:
            logging.info(f"Session success successfully established with: {self.host}")
            return resp.json().get('access_token')
        else:
            logging.warning(f"{resp.status_code} response code while trying to get bearer token from {self.base_url}")

    def set_bearer_auth(self, token: str):
        """
        Sets bearer auth
            Intended to be used with get_token, but will accept any valid the-one-api token

        Args:
            token: bearer auth token
        """
        self.session.headers['authorization'] = f'Bearer {token}'

    def build_url(self, resource: str) -> str:
        """
        Builds url

        Args:
            resource: path to the requested resource
        """
        if resource[0] != '/':
            resource = '/' + resource
        return self.base_url + resource

    def get_request(self, resource: str, params: dict = None) -> dict:
        """
        Executes basic get request

        Args:
            resource: path to the requested resource
            params: tuple of query parameters for the request
                can contain pagination, sorting, or filtering params

        Returns:
            dict containing results and pagination data
        """

        results = self.session.get(self.build_url(resource), params=params)
        if results.ok:
            return results.json()
        results.raise_for_status()

    def paginated_get_request(self, resource: str, params: dict = None) -> iter:
        """
        Executes paginated get request

        Args:
            resource: path to the requested resource
            params: tuple of query parameters for the request
                can contain pagination, sorting, or filtering params
                limit can be specified here to reduce the page size
                page can be specified here to change the starting page

        Returns:
            iterable yielding dicts containing results and pagination data
        """
        page = 0
        pages = 2000
        while page < pages:
            res = self.get_request(resource, params)
            pages = res['pages']
            page = res['page']
            yield res

    def get_movies(self, paginated: bool = False, params: dict = None) -> dict or iter:
        """
        Gets all movies from the api

        Args:
            paginated: bool specifying whether to return a generator yielding pages of data
            params: tuple of query parameters for the request
                can contain pagination, sorting, or filtering params
                sample params:
                {
                    'page': 2,
                    'limit': 10,
                    'budgetInMillions>2900': ''
                }

        Returns:
            dict containing results and pagination data
        """
        if paginated:
            return self.paginated_get_request('/v2/movie', params)
        return self.get_request('/v2/movie', params)

    def get_movie(self, movie_id: str, paginated: bool = False, params: dict = None) -> dict or iter:
        """
        Gets specific movie from the api
        Args:
            movie_id: id of the movie
            paginated: bool specifying whether to return a generator yielding pages of data
            params: tuple of query parameters for the request
                can contain pagination, sorting, or filtering params
        Returns:
            dict containing results and pagination data
        """
        resource = f'/v2/movie/{movie_id}'
        if paginated:
            return self.paginated_get_request(resource, params)
        return self.get_request(resource, params)

    def get_movie_quotes(self, movie_id: str, paginated: bool = False, params: dict = None) -> dict or iter:
        """
        Gets specific movie from the api
        Args:
            movie_id: id of the movie
            paginated: bool specifying whether to return a generator yielding pages of data
            params: tuple of query parameters for the request
                can contain pagination, sorting, or filtering params
                sample params:
                {
                    'page': 2,
                    'limit': 10,
                    'sort': 'name:desc'
                }
        Returns:
            generator yielding dict containing results and pagination data
        """
        resource = f'/v2/movie/{movie_id}/quote'
        if paginated:
            return self.paginated_get_request(resource, params)
        return self.get_request(resource, params)
