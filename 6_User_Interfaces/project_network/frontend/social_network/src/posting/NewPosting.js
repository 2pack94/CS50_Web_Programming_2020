import React from 'react';
import PropTypes from 'prop-types';
import { UserContext } from '../common/UserContext'
import { getCookie } from '../common/util'
import TextInput from '../common/TextInput'

class NewPosting extends React.Component {
    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            content: "",
            error: ""
        };
    }

    handleChange = (event) => {
        this.setState({content: event.target.value});
    }

    createPosting = (event) => {
        event.preventDefault();

        fetch('/api/postings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin',
            body: JSON.stringify({content: this.state.content})
        })
        .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
        .then(result => {
            if (!result.is_ok) {
                this.setState({error: result.body.error});
                return
            }
            this.setState({content: "", error: ""});
            this.props.onCreate();
        })
        .catch((err) => {
            console.log(err);
            this.setState({error: err.message});
        });
    }

    render() {
        if (!this.context.is_authenticated) {
            return null
        }
        return (
            <div className="container p-3 m-3 mx-auto border rounded">
                <h3>New Posting</h3>
                <div className="error-msg">{this.state.error}</div>
                <TextInput content={this.state.content}
                    handleChange={this.handleChange} handleSubmit={this.createPosting} />
            </div>
        );
    }
}

NewPosting.propTypes = {
    onCreate: PropTypes.func.isRequired
};

export default NewPosting
