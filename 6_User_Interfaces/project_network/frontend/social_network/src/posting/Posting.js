import React from 'react';
import PropTypes from 'prop-types';
import comment_icon from '../assets/comment-icon.png';
import { UserContext } from '../common/UserContext'
import { getCookie } from '../common/util'
import TextInput from '../common/TextInput'
import MultilineContent from '../common/MultilineContent'
import UserLink from './UserLink'
import LikeButton from './LikeButton'
import AllComments from './AllComments'

class Posting extends React.Component {
    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            // gets set to true if the posting is edited
            is_edit: false,
            // posting content when editing
            content_edit: "",
            // Clicking the comment button the first time sets mount_comments to true
            // and will mount the AllComments component.
            // Every next click will toggle the visibility of the AllComments component with hide_comments
            // so it will not get unmounted and request the comments again.
            mount_comments: false,
            hide_comments: false,
            error: ""
        };
    }

    handleChange = (event) => {
        this.setState({content_edit: event.target.value});
    }

    handleComment = () => {
        this.setState(state => ({
            mount_comments: true,
            hide_comments: !state.hide_comments
        }));
    }

    startEditing = () => {
        if (!this.state.is_edit) {
            this.setState({
                is_edit: true,
                content_edit: this.props.data.content,
                error: ""
            })
        }
    }

    cancelEditing = () => {
        this.setState({
            is_edit: false,
            content_edit: "",
            error: ""
        })
    }

    changePosting = (event) => {
        event.preventDefault();

        fetch(`/api/posting/${this.props.data.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin',
            body: JSON.stringify({content: this.state.content_edit})
        })
        .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
        .then(result => {
            if (!result.is_ok) {
                this.setState({error: result.body.error});
                return
            }
            this.setState({is_edit: false, content_edit: "", error: ""});
            // reload the posting data
            this.props.updatePosting(this.props.data.id);
        })
        .catch((err) => {
            console.log(err);
            this.setState({error: err.message});
        });
    }

    render() {
        return (
            <div className="container p-3 m-3 mx-auto border rounded">
                <div className="row">
                    <div className="col-10">
                        <UserLink user={this.props.data.user} user_id={this.props.data.user_id} />
                    </div>
                    {this.props.data.user_id === this.context.id && this.context.is_authenticated &&
                        <div className="col-2 text-right">
                            <button type="button" className="btn btn-link no-padding" onClick={this.startEditing}>
                                Edit
                            </button>
                        </div>
                    }
                </div>
                <div className="timestamp">Created {this.props.data.timestamp}</div>
                <div className="error-msg">{this.state.error}</div>
                {this.state.is_edit
                ? // if true
                    <TextInput content={this.state.content_edit} autofocus={true}
                        handleChange={this.handleChange} handleSubmit={this.changePosting}
                        handleCancel={this.cancelEditing} />
                : // else
                    <MultilineContent content={this.props.data.content} />
                }
                <hr />
                <div className="row my-1">
                    <div className="col">
                        {this.props.data.liked_by.length}
                        {this.props.data.liked_by.length === 1 ? " Like" : " Likes"}
                    </div>
                    <div className="col text-right">
                        {this.props.data.num_comments}
                        {this.props.data.num_comments === 1 ? " Comment" : " Comments"}
                    </div>
                </div>
                <div className="row my-1">
                    <div className="col text-center">
                        <LikeButton
                            id={this.props.data.id}
                            is_liked={this.props.data.liked_by.includes(this.context.id)}
                            updatePosting={this.props.updatePosting}
                        />
                    </div>
                    <div className="col text-center">
                        <button type="button" className="btn btn-link" onClick={this.handleComment}>
                            <img className="icon-24 mr-1" src={comment_icon} alt="" />
                            Comment
                        </button>
                    </div>
                </div>
                {this.state.mount_comments &&
                    <div style={{display: this.state.hide_comments ? null : 'none'}}>
                        <hr />
                        <AllComments posting={this.props.data.id} updatePosting={this.props.updatePosting} />
                    </div>
                }
            </div>
        );
    }
}

Posting.propTypes = {
    data: PropTypes.exact({
        id: PropTypes.number.isRequired,
        user: PropTypes.string.isRequired,
        user_id: PropTypes.number.isRequired,
        content: PropTypes.string.isRequired,
        timestamp: PropTypes.string.isRequired,
        liked_by: PropTypes.array.isRequired,
        num_comments: PropTypes.number.isRequired
    }),
    updatePosting: PropTypes.func.isRequired
};

export default Posting
