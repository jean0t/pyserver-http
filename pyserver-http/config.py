CRLF = "\r\n"
STANDARD_DECODE_ENCODE = "utf-8"

class StatusCode:
    SUCCESS = 200
    CREATED = 201
    
    NOTFOUND = 404

class StatusMessage:
    SUCCESS = "OK"
    CREATED = "Created"

    NOTFOUND = "Not Found"

class ContentType:
    PLAIN_TEXT = "text/plain"
    HTML = "text/html"
    
    FILE = "application/octet-stream"
