video: https://www.youtube.com/watch?v=opddeo3qvg8
notes: https://cs50.harvard.edu/web/2020/notes/6/
source code: http://cdn.cs50.net/web/2020/spring/lectures/6/src6.zip
assignment: https://cs50.harvard.edu/web/2020/projects/4/network/

Javascript History API: https://developer.mozilla.org/en-US/docs/Web/API/History
    Allows manipulation of the browser session history.
    The history.pushState() method is useful in single page applications to show the current URL
    and to navigate with the browser back and forward buttons.

Scroll:
    The following Parameters can be used to determine how far the page was scrolled:
        window.scrollY: How many pixels were scrolled from the top of the page.
        document.body.offsetHeight: The height in pixels of the entire document.
        window.innerHeight: Interior height of the window in pixels.
    This can be used to implement an infinite scroll feature.
    where more data gets loaded if the user scrolled to the bottom of the page.

CSS Animations: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations/Using_CSS_animations

/// React: https://reactjs.org/docs/getting-started.html

JSX:
    React uses JSX which is a syntax extension to JavaScript. Babel compiles JSX to Javascript.
    Every Tag must be closed explicitly. e.g.: <img ... />
    JSX Expressions must have one parent DOM element. e.g.: <div>...JSX-Code...</div>
    XSS attacks are prevented by escaping any values embedded in JSX before rendering them.

React Components:
    A React Application consists of components that contain the Markup and the logic.
    A component can be a function or a class inheriting from the React.Component class.
    A component takes a single object called "props" (Properties) as input (read-only) and returns a React Element.

React Elements:
    A React Element describes what should be rendered on the screen as HTML.
    Any valid JavaScript expression inside curly braces can be put in an element.
    Components can also be placed inside an Element, which allows for nesting Components.
    React elements are immutable.
    An Element or a list of Elements can also be assigned to a variable.
    Each item in an Element list needs a key (unique string) for React change detection.
    e.g.: let elem_list = [<li key="id_1">item1</li>, <li key="id_2">item2</li>];

State:
    A Component can be made stateful by assigning the this.state object.
    The state is updated by the this.setState() method, which will trigger a re-render of the Component.
    Any state change will only update the necessary parts of the DOM (possible through an in-memory virtual DOM).
    Data that can be computed from other data is not state. This data should be recalculated on every state change.

Events:
    React events are named using camelCase, rather than lowercase (e.g. onClick).
    Instead of using addEventListener, the callback function should be provided directly in the React Element.
    Its best to use the public class fields syntax for the callback function to have access to `this`.
    If the event handler needs to be called with parameters, use an arrow function.
        syntax: onClick={() => this.handleClick(param1)}

Forms:
    When React should handle the submission of the form and have access to the form data,
    the “controlled components” technique can be used.
    The value attribute of the form element should be set to the component state. e.g.: value={this.state.value}
    The onChange attribute should contain a callback function that updates the state.
    To prevent default behavior when submitting the form, the onSubmit callback must call preventDefault
    (return false does not work in React).

Lifting State Up:
    If there are 2 or more components who need the same data,
    a shared state should be moved to their closest common ancestor.
    The state, together with a method to change the state is passed as props to the child components.
    If the state change method gets called in a child component then all the other child components get updated too.

Containment:
    React Elements can be placed between an opening and closing Component Tag.
    These Elements get passed as a special children prop to the Component and can be rendered with {props.children}.

Component Lifecycle methods: https://reactjs.org/docs/react-component.html#the-component-lifecycle
    The following are the most common component lifecycle methods.
    componentDidMount(): called after a component is inserted into the DOM.
        order: constructor() -> render() -> componentDidMount()
    componentDidUpdate(): called on a props or state change (after render()).
    componentWillUnmount(): called when a component is being removed from the DOM.

Context: https://reactjs.org/docs/context.html
    Used when data needs to be accessible by many components at different nesting levels.
    This replaces the need of passing certain props to every Component.

Fragments: https://reactjs.org/docs/fragments.html
    Fragments can be used in a component to return multiple React elements.
    syntax: <React.Fragment>...JSX-Code...</React.Fragment> or <>...JSX-Code...</>

Refs: https://reactjs.org/docs/refs-and-the-dom.html
    Can be used to access DOM nodes or React elements created in the render method.

Type Checking:
    Runtime Type Checking with PropTypes: https://reactjs.org/docs/typechecking-with-proptypes.html
    Static Type Checking with Flow or Typescript: https://reactjs.org/docs/static-type-checking.html

React Router: https://reactrouter.com/web/guides/quick-start
    install with: $ npm install react-router-dom
