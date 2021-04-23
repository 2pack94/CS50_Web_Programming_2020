import React from 'react';
import PropTypes from 'prop-types';
import { Link } from "react-router-dom";
import { DELETED_USER_NAME } from '../common/UserContext'

// displays a Link with the username to the users profile page.
class UserLink extends React.Component {
    render() {
        return (
            <>
            {this.props.user === DELETED_USER_NAME
            ? // if true
                <b>{this.props.user}</b>
            : // else
                <Link to={`/profile/${this.props.user_id}`}>
                    <b>{this.props.user}</b>
                </Link>
            }
            </>
        )
    }
}

UserLink.propTypes = {
    user_id: PropTypes.number.isRequired,
    user: PropTypes.string.isRequired
};

export default UserLink
