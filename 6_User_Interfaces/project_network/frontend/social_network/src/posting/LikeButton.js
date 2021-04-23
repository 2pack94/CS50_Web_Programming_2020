import React from 'react';
import PropTypes from 'prop-types';
import { Redirect } from "react-router-dom";
import like_icon from '../assets/like-icon.png';
import { getCookie } from '../common/util'
import { UserContext } from '../common/UserContext'

class LikeButton extends React.Component {
    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            // specifies if the mouse is hovering over the button
            is_mouse_over: false,
            // if the user is not logged in and click the button, redirect him to the login page.
            redirect_to_login: false
        };
    }

    handleMouseOver = () => {
        this.setState({
            is_mouse_over: true
        });
    }

    handleMouseOut = () => {
        this.setState({
            is_mouse_over: false
        });
    }

    // toggle like status of the posting
    like = () => {
        if (!this.context.is_authenticated) {
            this.setState({
                redirect_to_login: true
            });
            return
        }
        fetch(`/api/posting/${this.props.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin',
            body: JSON.stringify({like: !this.props.is_liked})
        })
        .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
        .then(result => {
            if (!result.is_ok) {
                return
            }
            // reload posting data to show the new like number and update the like status.
            this.props.updatePosting(this.props.id);
        })
        .catch((err) => {
            console.log(err);
        });
    }

    render() {
        if (this.state.redirect_to_login) {
            return <Redirect to="/login" />
        }

        let button_text = "Like";
        if (this.props.is_liked) {
            button_text = "Liked";
            if (this.state.is_mouse_over) {
                button_text = "Unlike";
            }
        }

        return (
            <button type="button" className="btn btn-link text-left like-btn" onClick={this.like}
                onMouseOver={this.handleMouseOver} onMouseOut={this.handleMouseOut}
            >
                <img className="icon-24 mr-1" src={like_icon} alt="" />
                {button_text}
            </button>
        );
    }
}

LikeButton.propTypes = {
    id: PropTypes.number.isRequired,
    is_liked: PropTypes.bool.isRequired,
    updatePosting: PropTypes.func.isRequired
}

export default LikeButton
