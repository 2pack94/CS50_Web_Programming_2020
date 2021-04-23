import React from 'react';
import { Link, Redirect } from "react-router-dom";
import { getCookie } from '../common/util'
import { UserContext } from '../common/UserContext'

class Login extends React.Component {
    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: "",
            is_login: false,
            error: ""
        };
    }

    componentDidMount() {
        document.title = "Login - Network";
    }

    handleChange = (event) => {
        this.setState({[event.target.name]: event.target.value});
    }

    login = (event) => {
        event.preventDefault();

        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin',
            body: JSON.stringify({username: this.state.username, password: this.state.password})
        })
        .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
        .then(result => {
            if (!result.is_ok) {
                this.setState({error: result.body.error});
                return
            }
            this.context.getUser();
            this.setState({is_login: true, username: "", password: "", error: ""});
        })
        .catch((err) => {
            console.log(err);
            this.setState({error: err.message});
        });
    }

    render() {
        // redirect after the user logged in
        if (this.state.is_login) {
            return <Redirect to="/" />
        }
        return (
            <div>
            <h2>Login</h2>

            <div className="error-msg">{this.state.error}</div>

            <form method="post" onSubmit={this.login}>
                <div className="form-group">
                    <input autoFocus className="form-control" type="text" name="username"
                        value={this.state.username} onChange={this.handleChange} placeholder="Username"
                    />
                </div>
                <div className="form-group">
                    <input className="form-control" type="password" name="password"
                        value={this.state.password} onChange={this.handleChange} placeholder="Password"
                    />
                </div>
                <input className="btn btn-primary" type="submit" value="Login" />
            </form>

            Don't have an account? <Link to="/register">Register here.</Link>
            </div>
        );
    }
}

export default Login
