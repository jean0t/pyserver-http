# pyserver-http

pyserver-http is a lightweight HTTP server written in Python using only the standard library (socket and threading). It is designed with a clean and modular architecture based on the Router/Dispatcher design pattern, which keeps request routing, handling, and logging separate and easy to maintain.

## Table of Contents

- [Features](#features)
- [Architecture and Design Patterns](#architecture-and-design-patterns)
- [Endpoints](#endpoints)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [To-Do](#to-do)

## Features

- **Modular Architecture:** Divided into multiple files for easy maintainability:
  - `handler.py` – Contains the abstract `BaseHandler` and concrete `GetHandler` and `PostHandler` classes.
  - `route.py` – Implements the `Router` class to map routes to handlers.
  - `request.py` – Contains the `Request`, `Parser`, and `Response` classes for handling HTTP data.
  - `log.py` – Provides logging capabilities via the `Log` class.
  - `config.py` – Stores configuration variables such as status codes, status messages, CRLF, and encoding constants.
  - `main.py` – Entry point for the server.
- **Supports GET and POST:** Routes are dynamically dispatched based on the HTTP method.
- **File Handling:** 
  - GET `/files/<filename>` returns the file for download.
  - POST `/file` creates a file with the content provided in the request body.
- **Dynamic Endpoints:** 
  - `/` returns a simple 200 OK response.
  - `/user-agent` returns the user agent of the user.
  - `/echo/<message>` returns the `<message>` as the response body.
- **Threading Support:** Uses threading to accept multiple simultaneous requests.
- **Command-Line Option:** Supports a `--directory` argument to change the base directory for file operations.
- **No Third-Party Libraries:** Built entirely with Python’s standard library.

## Architecture and Design Patterns

pyserver-http is built using a combination of design patterns that help keep concerns separated and the code modular:

- **Router/Dispatcher Pattern:**  
  The `Router` class in `route.py` maintains a dictionary where the keys are tuples of HTTP method and URL path (e.g., `("GET", "/")`). It dispatches requests to the appropriate handler based on the route.

- **Strategy Pattern (via Handlers):**  
  The abstract `BaseHandler` (in `handler.py`) defines the basic structure for handling requests. Two concrete classes, `GetHandler` and `PostHandler`, extend this base class and implement request-specific logic. Each handler class includes methods (e.g., `root`, `echo`, etc.) that are dynamically called based on the request path.

- **Template Method Pattern:**  
  The `BaseHandler` also employs a template method pattern by providing a framework for building HTTP responses. Subclasses override specific methods to define their own behavior while reusing the common response-building logic.

- **Logging and Configuration Separation:**  
  The `Log` class in `log.py` and constants in `config.py` ensure that logging and configuration details are not hard-coded within the core logic.

## Endpoints

- **GET /**
  - **Description:** Returns a 200 OK response.
  - **Response:** Simple HTML page indicating success.

- **GET /echo/\<message\>**
  - **Description:** Returns the text following `/echo/` as the body.
  - **Example:**  
    Request: `GET /echo/abc`  
    Response Body: `abc`

- **GET /user-agent**
  - **Description:** Returns the user agent as the body.
  - **Example:**  
    Request: `GET /user-agent`  
    Response Body: `Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.38 Mobile Safari/537.36`

- **GET /files/\<filename\>**
  - **Description:** Serves the requested file for download.
  - **Note:** The base directory can be modified using the `--directory` command-line argument (default is `/files`).

- **POST /fileis/\<filename\>**
  - **Description:** Creates a file using the contents of the request body and name as the filename specified.
  - **Usage:** The file is written to the directory specified by the `--directory` argument (default is /files).

## Project Structure

```
pyserver-http/
├── config.py      # Configuration constants (StatusCode, CRLF, etc.)
├── handler.py     # BaseHandler, GetHandler, and PostHandler classes
├── log.py         # Log class for logging functionality
├── request.py     # Request, Parser, and Response classes for HTTP handling
├── route.py       # Router class to manage and dispatch routes
└── main.py        # Main entry point to start the server
```

## Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jean0t/pyserver-http.git
   cd pyserver-http
   ```

2. **Run the server:**

   ```bash
   python -m pyhttp-server [--directory /another/path]
   ```

3. **Test the endpoints:**

   - Access `http://localhost:4221/` for a 200 OK response.
   - Use `curl` or a browser to test `/echo/<message>`, `/files/<filename>`, or send a POST request to `/files/<filename>`.

## Contributing

Contributions and forks are available and encouraged! If you'd like to contribute to pyserver-http, please fork the repository and submit a pull request. We welcome improvements, bug fixes, and feature suggestions.

## License

pyserver-http is licensed under the GPL-3 license. See the [LICENSE](LICENSE) file for details.

## To-Do

- **Gzip Encoding/Decoding:** Implement gzip support for request and response bodies.
- **Further Testing:** Additional testing and improvements in error handling.
- **Enhancements:** Consider more robust routing (e.g., regex-based) and additional HTTP methods.

---

Feel free to reach out or open an issue if you have any questions or suggestions!

