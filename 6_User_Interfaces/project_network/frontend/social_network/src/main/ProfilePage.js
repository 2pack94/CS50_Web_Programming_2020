import React from 'react';
import { withRouter } from "react-router";
import { getCookie } from '../common/util'
import { UserContext } from '../common/UserContext'
import PostingList from '../posting/PostingList';

class ProfilePage extends React.Component {
    static contextType = UserContext;

    constructor(props) {
        super(props);
        this.state = {
            username: "",
            num_following: 0,
            num_followers: 0,
            // true if the current user followed the user of this profile
            is_followed: false,
            error: ""
        };
        // The match parameter "id" was specified in the Route path (see App.js).
        this.user_id = parseInt(this.props.match.params.id, 10);
    }

    componentDidMount() {
        this.getProfile();
    }

    getProfile = () => {
        if (isNaN(this.user_id)) {
            this.setState({error: "Page not found"});
            return
        }
        fetch(`/api/profile/${this.user_id}`)
        .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
        .then(result => {
            if (!result.is_ok) {
                this.setState({error: result.body.error});
                return
            }
            document.title = `${result.body.username} - Network`;

            this.setState({
                username: result.body.username,
                num_following: result.body.num_following,
                num_followers: result.body.num_followers,
                is_followed: result.body.is_followed,
                error: ""
            });
        })
        .catch((err) => {
            console.log(err);
            this.setState({error: err.message});
        });
    }

    follow = () => {
        fetch(`/api/profile/${this.user_id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin',
            body: JSON.stringify({follow: !this.state.is_followed})
        })
        .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
        .then(result => {
            if (!result.is_ok) {
                console.log(result.body.error);
                return
            }
            this.getProfile();
        })
        .catch((err) => {
            console.log(err);
        });
    }

    render() {
        // if the user id in the url changed, reload the profile data.
        let user_id_prev = this.user_id;
        this.user_id = parseInt(this.props.match.params.id, 10);
        if (this.user_id !== user_id_prev) {
            this.getProfile();
            return null
        }
        if (this.state.error !== "") {
            return <div className="error-msg text-center my-2">{this.state.error}</div>
        }
        // render only after the response was received
        if (this.state.username === "") {
            return null
        }
        return (
            <div className="container mx-auto">
                <div className="container m-3 p-3 mx-auto border rounded">
                    <div className="row">
                        <div className="col-10">
                            <h3>{this.state.username}</h3>
                        </div>
                        {this.user_id !== this.context.id && this.context.is_authenticated &&
                            <div className="col-2 text-right">
                                <button type="button" className="btn btn-primary" onClick={this.follow}>
                                    {this.state.is_followed ? "Unfollow" : "Follow"}
                                </button>
                            </div>
                        }
                    </div>
                    <div>
                        {this.user_id === this.context.id
                        ? // if true
                            `You have ${this.state.num_followers}`
                        : // else
                            `${this.state.username} has ${this.state.num_followers}`
                        }
                        {this.state.num_followers === 1 ? " Follower" : " Followers"}
                    </div>
                    <div>
                        {this.user_id === this.context.id
                        ? // if true
                            `You are following ${this.state.num_following}`
                        : // else
                            `${this.state.username} is following ${this.state.num_following}`
                        }
                        {this.state.num_following === 1 ? " Person" : " People"}
                    </div>
                </div>
                <h3 className="mt-3">Postings</h3>
                {/* The key prop is needed to mount a new instance of the component when the user id changes. */}
                <PostingList key={this.user_id} user={this.user_id} />
            </div>
        )
    }
}

export default withRouter(ProfilePage)
