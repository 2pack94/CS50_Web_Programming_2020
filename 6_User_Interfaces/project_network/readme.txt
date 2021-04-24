separated Back- and Frontend:
    A Frontend can be served up together with the Backend.
    Javascript or the React Framework can be used inside the Django templates.
    The other possibility is to serve up the Frontend separately from the backend.
    Advantages separated Back- and Frontend:
        - easier to scale, because backend and frontend servers can be scaled at a separate pace.
        - allows for a frontend in a mobile app.
    Disadvantages separated Back- and Frontend:
        - Django Template features (variables) can't be used.
        - CORS must be configured.
    This project will use a separated Back- and Frontend as described in this example:
    https://testdriven.io/blog/django-spa-auth/
    # The frontend was created by running: https://reactjs.org/docs/create-a-new-react-app.html#create-react-app
    $ npx create-react-app social_network

REST API:
    A popular approach for implementing the communication between backend and frontend is using a REST API.
    Django REST Framework: https://www.django-rest-framework.org/tutorial/1-serialization/
    This project will not use Django REST Framework however. The JSON data transfer will be implemented manually.

Authentication:
    This project will use the default session-based Authentication.
    Because the Back- and Frontend are separated, the user and session data must be fetched with Ajax from the server.
    The more popular solution, especially with separated Back- and Frontend (e.g. mobile app frontend),
    is Token-based Authentication.

Token-based Authentication:
    After logging in, the server validates the credentials and, if valid, creates and sends back a signed token to the browser.
    In most cases, the token is stored in localStorage.
    The client then adds the token to the header when a request is made to the server.
    Assuming the request came from an authorized source, the server decodes the token and checks its validity.
    The most common type of token is a JSON Web Token (JWT). https://jwt.io/introduction
    Available in Django REST Framework: https://www.django-rest-framework.org/api-guide/authentication/

CORS (Cross-origin resource sharing):
    https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy
    If the Frontend is served up separately from the Backend, CORS will play a role.
    A web browser permits scripts contained in a first web page to access data
    in a second web page only if both web pages have the same origin.
    An origin is defined as a combination of protocol, port, and host.
    Ajax requests are forbidden by default by the same-origin security policy.
    CORS works by requiring the server to include a specific set of headers
    that allow a browser to determine if and when cross-domain requests should be allowed.
    Browsers make a “preflight” request to the server hosting the cross-origin resource,
    in order to check that the server will permit the actual request.
    In response, the server sends back an Access-Control-Allow-Origin header.
    By default, in cross-site Ajax invocations, browsers will not send credentials (This includes the Django session Cookies).
    The response to a preflight request must specify Access-Control-Allow-Credentials: true
    to indicate that the actual request can be made with credentials.
    Add CORS headers to responses in Django: https://github.com/adamchainz/django-cors-headers

nginx:
    http://nginx.org/en/docs/beginners_guide.html
    https://linuxize.com/post/nginx-reverse-proxy/
    nginx can be used as a reverse proxy server to expose both the Back- and Frontend under the same host and port.
    This eliminates CORS Errors between Back- and Frontend.
    A reverse proxy server is a type of proxy server that typically sits behind the firewall
    in a private network and directs client requests to the appropriate backend server.
    It then fetches and delivers the server’s response back to the client.
    A reverse proxy server can act as a load balancer to redirect traffic to multiple backend servers.
    nginx also caches the content received from the proxied servers' responses (speed increase).

Setup:
    # Install all frontend packages defined in package.json into the node_modules folder.
    # In this case this is done on the host system and not in the Dockerfile for easier setup.
    # In frontend folder (needed one-time):
    $ npm install
    # In project root folder:
    $ sudo docker-compose up
    # Alternatively rebuild all containers (--build) and start in detached mode (-d):
    $ sudo docker-compose up --build -d
    Access the Website with: http://127.0.0.1:81/
