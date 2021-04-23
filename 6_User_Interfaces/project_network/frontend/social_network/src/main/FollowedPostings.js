import React from 'react';
import { Redirect } from "react-router-dom";
import { UserContext } from '../common/UserContext';
import PostingList from '../posting/PostingList';

class FollowedPostings extends React.Component {
    static contextType = UserContext;

    componentDidMount() {
        document.title = "Following - Network";
    }

    render() {
        if (!this.context.is_authenticated) {
            return <Redirect to="/" />
        }
        return (
            <div className="container mt-1 no-padding">
                <h2>Followed Postings</h2>
                <PostingList following={true} />
            </div>
        );
    }
}

export default FollowedPostings
