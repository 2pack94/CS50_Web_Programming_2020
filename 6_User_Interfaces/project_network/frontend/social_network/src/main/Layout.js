import React from 'react';
import PropTypes from 'prop-types';
import { Link } from "react-router-dom";
import { UserContext } from '../common/UserContext'

class Layout extends React.Component {
    static contextType = UserContext;

    render() {
        return (
            <div>
            <nav className="navbar navbar-expand-sm navbar-light sticky-top bg-light">
                <Link to={"/"} className="navbar-brand">Network</Link>
                <div>
                    <ul className="navbar-nav mr-auto">
                        {this.context.is_authenticated &&
                            <li className="nav-item">
                                <Link to={`/profile/${this.context.id}`} className="nav-link">
                                    <strong>{this.context.username}</strong>
                                </Link>
                            </li>
                        }
                        <li className="nav-item">
                            <Link to="/" className="nav-link">All Postings</Link>
                        </li>
                        {this.context.is_authenticated
                        ? // if true
                            <>
                            <li className="nav-item">
                                <Link to="/following" className="nav-link">Following</Link>
                            </li>
                            <li className="nav-item">
                                <Link to="/logout" className="nav-link">Log Out</Link>
                            </li>
                            </>
                        : // else
                            <>
                            <li className="nav-item">
                                <Link to="/login" className="nav-link">Log In</Link>
                            </li>
                            <li className="nav-item">
                                <Link to="/register" className="nav-link">Register</Link>
                            </li>
                            </>
                        }
                    </ul>
                </div>
            </nav>
            <div className="container-fluid">
                {this.props.children}
            </div>
            </div>
        )
    }
}

Layout.propTypes = {
    children: PropTypes.node.isRequired,
};

export default Layout
