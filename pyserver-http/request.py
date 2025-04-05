from .config import CRLF, STANDARD_DECODE_ENCODE
from .route import Router
from .handler import GetHandler, PostHandler

class Parser:
    """
    Helper class to Request, helps parsing useful information that will be used while making the reply
    to the client request.
    """
    def __init__(self, content):
        self.header_raw, _, self.body = content.partition(CRLF * 2)
        self.http_header, self.headers = self.header_raw.split(CRLF)[0], {k.split(": ")[0]: k.split(": ")[1] for k in self.header_raw.split(CRLF)[1:]}
        self.method, self.path, self.protocol = self.http_header.split(" ")
        self.base_path, self.rest_path = self.parse_path()
    
    def parse_path(self):
        tmp = self.path.strip("/").split("/", 1) # /echo/abc/dcs -> ['echo', 'abc/dcs']
        if not tmp[0]:
            return "/", ""
        
        elif len(tmp) < 2:
            return "/" + tmp[0], ""
        
        return "/" + tmp[0], tmp[1]

class Request:
    """
    Responsible to get the bytes from the client request and forming an answer to reply accordingly.
    """

    def __init__(self, payload, file_directory):
        self.request = Parser(payload.decode(STANDARD_DECODE_ENCODE))
        self.router = Router()
        self._get_handler = GetHandler(file_directory)
        self._post_handler = PostHandler(file_directory)
        self._add_routes()

    def _add_routes(self):
        # GET REQUESTS
        self.router.add_route("GET", "/", self._get_handler.root)
        self.router.add_route("GET", "/echo", self._get_handler.echo)
        self.router.add_route("GET", "/user-agent", self._get_handler.user_agent)
        self.router.add_route("GET", "/files", self._get_handler.files)

        # POST REQUESTS
        self.router.add_route("POST", "/files", self._post_handler.files)


    def Request(self) -> bytes:
        if self.request.method == "GET":
            return self.router.route(self.request.method, self.request.base_path)(self.request.headers, self.request.rest_path)
        
        else:
            return self.router.route(self.request.method, self.request.base_path)(self.request.headers, self.request.rest_path, self.request.body)

