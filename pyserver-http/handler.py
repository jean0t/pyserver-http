import gzip

from base64 import b64encode
from abc import ABC, abstractmethod
from .config import StatusCode, StatusMessage, ContentType, CRLF, STANDARD_DECODE_ENCODE, accepted_encoding
from pathlib import Path, PosixPath
from typing import Dict

class BaseHandler(ABC):
    def __init__(self, file_directory: PosixPath, headers: Dict):
        self.compression = False
        self.status_code = StatusCode.SUCCESS
        self.status_message = StatusMessage.SUCCESS
        self.headers = {}
        self.body = ''
        self.file_directory = Path(__file__).parent / file_directory
        self.request_headers = headers

        self.encoding = self.request_headers.get("Accept-Encoding", "").split(",")
        if any([x.strip() in accepted_encoding for x in self.encoding]):
            self.accept_compression()
    
    def accept_compression(self):
        self.compression = True
        self.headers["Content-Encoding"] = "gzip"

    @abstractmethod
    def build_response(self):
        pass

    @staticmethod
    def unknown(target: str):
        return "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>\r\n".encode(STANDARD_DECODE_ENCODE)


class GetHandler(BaseHandler):
    """
    Class that inherits from BaseHandler to create a standard interface
    to interact with GET requests, provides handlers according to the path
    """

    def __init__(self, file_directory: PosixPath, headers: Dict):
            super().__init__(file_directory, headers)
            

    def build_response(self):
        r"""
        Build a general response that will depends on the variable self.headers, self.body, self.status_code and self.status_message.
        The response is given in bytes with the format:
        HTTP HEADER\r\n
        HEADERS\r\n
        BODY\r\n
        obs: BODY is optional, in this case the last line wont exist
        """
        header_list = []
        for k, v in self.headers.items():
            header_list.append(f"{k}: {v}")
        
        if self.compression is True and self.body != "": 
            self.body = gzip.compress(self.body.encode(STANDARD_DECODE_ENCODE))
            if self.headers.get("Content-Length", None):
                self.headers["Content-Length"] = len(self.body) + 2 # + 2 due to the CRLF \r\n -> 2 bytes

        message = Response.build_message(self.status_code, self.status_message, self.headers, self.body, self.compression)
        return message
    
    def root(self, target: str):
        """
        Return for the route /
        """
        self.headers = self.request_headers
        return self.build_response()

    def echo(self, target: str):
        """
        Return for the route /echo
        """
        
        self.headers["Content-Type"] = ContentType.PLAIN_TEXT
        self.headers["Content-Length"] = len(target)
        self.body = target
        return self.build_response()
    
    def user_agent(self, target: str):
        """
        Return for the route /user-agent
        """
        filter = "User-Agent"
        self.headers["Content-Type"] = ContentType.PLAIN_TEXT
        self.headers["Content-Length"] = len(self.request_headers[filter])
        self.body = self.request_headers[filter]
        return self.build_response()


    def files(self, target: str):
        """
        Return for the route /files
        """
        file = self.file_directory / target
        if file.exists() and file.is_file():
            file_contents = file.read_text()
            self.headers["Content-Type"] = ContentType.FILE
            self.headers["Content-Length"] = len(file_contents.replace("\n", ""))
            self.body = file_contents
            return self.build_response()
        else:
            self.status_code = StatusCode.NOTFOUND
            self.status_message = StatusMessage.NOTFOUND
            return self.build_response()
    



class PostHandler(BaseHandler):
    """
    Class that inherits from BaseHandler to create a standard interface
    to interact with POST requests, provides handlers according to the path
    """

    def __init__(self, file_directory: PosixPath, headers: Dict):
            super().__init__(file_directory, headers)

    def build_response(self):
        r"""
        Build a general response that will depends on the variable self.headers, self.body, self.status_code and self.status_message.
        The response is given in bytes with the format:
        HTTP HEADER\r\n
        HEADERS\r\n
        BODY\r\n
        obs: BODY is optional, in this case the last line wont exist
        """
        header_list = []
        for k, v in self.headers.items():
            header_list.append(f"{k}: {v}")
        message = f"{Response.build_message(self.status_code, self.status_message, self.headers, self.body)}"
        return message.encode(STANDARD_DECODE_ENCODE)
    
    def files(self, target: str, body: str):
        self.status_code, self.status_message = StatusCode.CREATED, StatusMessage.CREATED
        if self.request_headers["Content-Type"] == ContentType.FILE:
            file = self.file_directory / target
            file.write_text(body)
            return self.build_response()
            



class Response:
    """
    Auxiliary Class to build response.
    """

    @staticmethod
    def build_http(status_code: int, status_message: str) -> bytes:
        return f"HTTP/1.1 {status_code} {status_message}{CRLF}".encode(STANDARD_DECODE_ENCODE)

    @staticmethod
    def build_headers(headers: Dict) -> bytes:
        header_list = [f"{k}: {headers[k]}" for k in headers]
        return f"{CRLF.join(header_list)}{CRLF if header_list else ''}{CRLF}".encode(STANDARD_DECODE_ENCODE)

    @staticmethod
    def build_body(body: str|bytes, compression: bool) -> bytes:
        if compression:
            return body + CRLF.encode(STANDARD_DECODE_ENCODE)
        return f"{body}{CRLF if body else ''}".encode(STANDARD_DECODE_ENCODE)
    
    @staticmethod
    def build_message(status_code: int, status_message: str, headers: Dict, body: str, compression = False) -> bytes:
        return Response.build_http(status_code, status_message) + Response.build_headers(headers) + Response.build_body(body, compression)