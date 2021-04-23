import React from 'react';
import { Link, Redirect } from "react-router-dom";
import { getCookie } from '../common/util'
import { UserContext } from '../common/UserContext'

class Register extends React.Component {
    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            username: "",
            email: "",
            password: "",
            confirmation: "",
            is_register: false,
            error: "",
        };
    }

    componentDidMount() {
        document.title = "Register - Network";
    }

    handleChange = (event) => {
        this.setState({[event.target.name]: event.target.value});
    }

    register = (event) => {
        event.preventDefault();

        fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin',
            body: JSON.stringify({
                username: this.state.username,
                email: this.state.email,
                password: this.state.password,
                confirmation: this.state.confirmation
            })
        })
        .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
        .then(result => {
            if (!result.is_ok) {
                this.setState({error: result.body.error});
                return
            }
            this.context.getUser();
            this.setState({is_register: true, username: "", email: "",
                password: "", confirmation: "", error: ""});
        })
        .catch((err) => {
            console.log(err);
            this.setState({error: err.message});
        });
    }

    render() {
        // redirect after the user registered
        if (this.state.is_register) {
            return <Redirect to="/" />
        }
        return (
            <div >
            <h2>Register</h2>

            <div className="error-msg">{this.state.error}</div>

            <form method="post" onSubmit={this.register}>
                <div className="form-group">
                    <input className="form-control" autoFocus type="text" name="username"
                        value={this.state.username} onChange={this.handleChange} placeholder="Username" />
                </div>
                <div className="form-group">
                    <input className="form-control" type="email" name="email"
                        value={this.state.email} onChange={this.handleChange} placeholder="Email Address" />
                </div>
                <div className="form-group">
                    <input className="form-control" type="password" name="password"
                        value={this.state.password} onChange={this.handleChange} placeholder="Password" />
                </div>
                <div className="form-group">
                    <input className="form-control" type="password" name="confirmation"
                        value={this.state.confirmation} onChange={this.handleChange} placeholder="Confirm Password" />
                </div>
                <input className="btn btn-primary" type="submit" value="Register" />
            </form>
            
            Already have an account? <Link to="/login">Log In here.</Link>
            </div>
        );
    }
}

export default Register
