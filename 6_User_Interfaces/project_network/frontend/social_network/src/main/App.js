import React from 'react';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import './App.css';
import Layout from './Layout'
import Login from './Login'
import Register from './Register'
import Logout from './Logout'
import AllPostings from './AllPostings'
import FollowedPostings from './FollowedPostings'
import ProfilePage from './ProfilePage'
import { UserContext } from '../common/UserContext'


class App extends React.Component {
    constructor(props) {
        super(props);

        // This state represents UserContext
        this.state = {
            id: 0,
            is_authenticated: false,
            username: "",
            getUser: this.getUser,
            resetUser: this.resetUser
        }
    }

    componentDidMount() {
        // Get information of the current user on startup.
        // This initial request to the backend is also needed to get the Cookie containing the CSRF token.
        // This Cookie will then be used in the next POST/ PUT request.
        this.getUser();
    }

    getUser = () => {
        fetch("/api/user")
        .then(response => response.json())
        .then(result => {
            this.setState({
                id: result.id,
                is_authenticated: result.is_authenticated,
                username: result.username,
            });
        })
        .catch((err) => {
            console.log(err);
        });
    }

    resetUser = () => {
        this.setState({
            id: 0,
            is_authenticated: false,
            username: "",
        });
    }

    render() {
        return (
            <UserContext.Provider value={this.state}>
            <Router>
                <Switch>
                    <Route path="/login">
                        <Layout>
                            <Login />
                        </Layout>
                    </Route>
                    <Route path="/register">
                        <Layout>
                            <Register />
                        </Layout>
                    </Route>
                    <Route path="/logout">
                        <Layout>
                            <Logout />
                        </Layout>
                    </Route>
                    <Route path="/profile/:id">
                        <Layout>
                            <ProfilePage />
                        </Layout>
                    </Route>
                    <Route path="/following">
                        <Layout>
                            <FollowedPostings />
                        </Layout>
                    </Route>
                    <Route path="/">
                        <Layout>
                            <AllPostings />
                        </Layout>
                    </Route>
                </Switch>
            </Router>
            </UserContext.Provider>
        );
    }
}

export default App;
