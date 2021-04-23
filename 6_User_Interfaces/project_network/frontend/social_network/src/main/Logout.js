import React from 'react';
import { Redirect } from "react-router-dom";
import { UserContext } from '../common/UserContext'

class Logout extends React.Component {
    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            is_logout: false
        };
    }

    componentDidMount() {
        this.logout();
    }

    logout = () => {
        fetch('/api/logout')
        .then(() => {
            this.setState({is_logout: true});
            this.context.resetUser();
        })
        .catch((err) => {
            console.log(err);
        });
    }

    render() {
        // redirect after the user logged out
        if (this.state.is_logout) {
            return <Redirect to="/" />
        }
        return null
    }
}

export default Logout
