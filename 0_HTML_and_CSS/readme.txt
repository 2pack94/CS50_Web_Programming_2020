video: https://www.youtube.com/watch?v=zFZrkCIc2Oc&feature=youtu.be
notes: https://cs50.harvard.edu/web/2020/notes/0/
source code: http://cdn.cs50.net/web/2020/spring/lectures/0/src0.zip
assignment: https://cs50.harvard.edu/web/2020/projects/0/search/

HTML (Hypertext Markup Language):
    defines the structure of the Web page
    HTML elements consist of opening and closing tags (some Elements are self-closing tags, like <img>)
    HTML elements can include attributes, which give extra information about the element
    To be able to reference specific HTML ELements, the attribute "class" or "id" can be used
        id: no two elements can have the same id, and no element can have more than one id.
        class: can be shared by more than one element, and a single element can have more than one class
    List of HTML Tags: https://www.w3schools.com/tags/ref_byfunc.asp
    Document Object Model (DOM): describes how HTML elements relate to each other using a tree-like structure

CSS (Cascading Style Sheets):
    defines the style of the Web page
    CSS properties can be added in the following ways:
        add a style attribute to a HTML element (inline). Mixing CSS and HTML code like this is not ideal design.
        add CSS between <style> tags inside the HTML head. Specify the HTML Tags and how they shall be styled
        use a stylesheet (.css file) and create a link to it in the HTML head
    list of CSS properties: https://www.w3schools.com/cssref/
    CSS selectors:
        https://www.w3schools.com/cssref/css_selectors.asp
        patterns used to select the element(s) you want to style.
        HTML id's, classes, types or specific combinations of types can be selected
    CSS Specificity:
        If there is an HTML Element that is selected by multiple conflicting CSS,
        the following priority order is applied (specific to unspecific): In-line styling, id, class, element type

Responsive Design:
    makes sure that the Web page is displayed nicely no matter the screen size (Desktop or Mobile)
    viewport: https://www.w3schools.com/css/css_rwd_viewport.asp
    media query (@media): https://www.w3schools.com/cssref/css3_pr_mediaquery.asp
    flexbox: https://www.w3schools.com/css/css3_flexbox.asp
    grid: https://www.w3schools.com/css/css_grid.asp

Bootstrap: https://getbootstrap.com/docs/4.6/getting-started/introduction/
    CSS library with pre-defined components
    bootstrap implements responsiveness by using a grid system: https://getbootstrap.com/docs/4.6/layout/grid/
    add a link to the bootstrap stylesheet inside the HTML head.
    add a HTML class attribute (defined in the bootstrap component documentation) to apply the styling

Sass (Syntactically Awesome Style Sheets): https://sass-lang.com/documentation
    Extension to CSS with more features and cleaner syntax
    A Sass file (.scss file) must be compiled into a CSS file (.css file) in order to link it to a HTML file.
    $ sass stylesheet.scss:stylesheet.css
    By using the flag --watch, Sass will watch the file and automatically compile when it changes
    Sass provides the following features: Variables, Nesting CSS Selectors, Inheritance, ...
