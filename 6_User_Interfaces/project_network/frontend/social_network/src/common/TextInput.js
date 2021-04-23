import React from 'react';
import PropTypes from 'prop-types';

class TextInput extends React.Component {
    constructor(props) {
        super(props);

        this.textarea_ref = React.createRef();
        this.padding_x = 10;
        this.textarea_max_height = 208;
        this.CONTENT_MAX_LENGTH = 300;
    }

    adjustSize = () => {
        // Adjust textarea height to content size.
        // First set the height to 0, so the scroll height can be used to calculate the required height.
        this.textarea_ref.current.style.height = "0px";
        this.textarea_ref.current.style.height =
            Math.min(this.padding_x + this.textarea_ref.current.scrollHeight, this.textarea_max_height) + "px";
    }

    handleChange = (event) => {
        this.props.handleChange(event);
        // Javascript form validation: https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation
        // setCustomValidity adds a custom error message to the element and marks the element
        // as invalid so that the form cannot be submitted. The error styling is done automatically by the browser.
        // A more sophisticated solution offers the form library for React "Formik".
        if (event.target.value.length > this.CONTENT_MAX_LENGTH) {
            event.target.setCustomValidity(
                `Max ${this.CONTENT_MAX_LENGTH} characters allowed (currently ${event.target.value.length})`);
        } else {
            event.target.setCustomValidity("");
        }
    }

    componentDidMount() {
        this.adjustSize();
    }

    componentDidUpdate() {
        this.adjustSize();
    }

    render() {
        return (
            <form method="post" onSubmit={this.props.handleSubmit}>
                <textarea ref={this.textarea_ref} autoFocus={this.props.autofocus}
                    className="form-control no-resize" placeholder="Write something"
                    name="content" value={this.props.content} onChange={this.handleChange}>
                </textarea>
                <input type="submit" className="btn btn-primary mt-1 mr-1" disabled={!this.props.content}
                    name="post" value={this.props.post_btn_value} />
                {this.props.handleCancel &&
                    <input type="button" className="btn btn-primary mt-1 mr-1" name="cancel" value="Cancel"
                        onClick={this.props.handleCancel} />
                }
            </form>
        )
    }
}

TextInput.defaultProps = {
    post_btn_value: "Post"
};

TextInput.propTypes = {
    content: PropTypes.string.isRequired,
    post_btn_value: PropTypes.string,
    autofocus: PropTypes.bool,
    handleChange: PropTypes.func.isRequired,
    handleSubmit: PropTypes.func.isRequired,
    handleCancel: PropTypes.func
};

export default TextInput
