video: https://www.youtube.com/watch?v=x5trGVMKTdY
notes: https://cs50.harvard.edu/web/2020/notes/5/
source code: cdn.cs50.net/web/2020/spring/lectures/5/src5.zip
assignment: https://cs50.harvard.edu/web/2020/projects/3/mail/

Debugging:
    In the Browser Console the Javascript code can be debugged.
    Javascript code can be typed into the console.
    The current DOM and Javascript code can be manipulated.

Variables:
    var: global scope when defined outside of a function. function scope when defined inside of a function.
    let: block {} scope.
    const: block {} scope. defines a constant reference to a value (the properties of the object can still be changed).
    Declaring a variable without a keyword is not recommended,
    because it can accidentally overwrite a global variable with the same name.

HTML DOM Document: https://www.w3schools.com/js/js_htmldom_document.asp
    owner of all objects in the web page.
    is used to access and manipulate HTML.
    List of properties and methods that can be used on HTML documents:
        https://www.w3schools.com/jsref/dom_obj_document.asp

querySelector: https://www.w3schools.com/jsref/met_document_queryselector.asp
    document.querySelector() searches for and returns DOM Element objects (HTML element).
    The syntax to select a HTML Element is the same as for CSS selectors.
    List of properties and methods that can be used on all HTML elements:
        https://www.w3schools.com/jsref/dom_obj_all.asp
    The properties of a HTML element can also be seen when printing it to the console.
    HTML Event Attributes can be accessed and a callback function can be registered for that Event.
    List of HTML Events: https://www.w3schools.com/tags/ref_eventattributes.asp
    The addEventListener() method can also be used to add a callback for an event.
    The event name must be specified without the "on" prefix here.

DOMContentLoaded:
    Accessing HTML Elements directly when loading the page will not work,
    because it takes some time for the page to load.
    The following function can be used to register a callback function that only runs after the page has been loaded.
    In the callback function the HTML Elements can be accessed.
    document.addEventListener('DOMContentLoaded', callback_function_name)

HTML data attributes: https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes

Storage: https://developer.mozilla.org/en-US/docs/Web/API/Storage
    Storage allows to store key-value pairs in a database of the browser. The data is tied to the domain.
    Storage can be viewed in the developer tools of the Browser.
    sessionStorage:  Stored for the current session (until the browser is closed).
    localStorage: Persistent across different sessions.

Javascript Objects: https://www.w3schools.com/js/js_objects.asp
    Similar to a python dictionary with similar syntax.
    JSON (JavaScript Object Notation) is often used to exchange data between Internet Services.

Sending AJAX (Asynchronous JavaScript and XML) requests to a webserver with fetch():
    https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

Javascript functions:
    https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions#comparing_traditional_functions_to_arrow_functions
    arrow functions: () => {}
        Arrow functions establish "this" based on the scope the Arrow function is defined within.
    traditional functions: function() {}
        The value of the "this" keyword is is set to the object that called the function.
        If there was no explicit caller, then "this" is defined by the calling environment.
        When used as an Object Method, "this" will be the object that owns the function.
        When used as a HTML event handler, "this" refers to the HTML element that received the event.

Miscellaneous Javascript Concepts:
    Computed Property Names:
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Object_initializer#computed_property_names
    Import/ Export:
        https://developer.mozilla.org/en-US/docs/web/javascript/reference/statements/export
    Array Destructuring:
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment
