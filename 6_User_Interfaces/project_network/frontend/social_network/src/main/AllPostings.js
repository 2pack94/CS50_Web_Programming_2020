import React from 'react';
import PostingList from '../posting/PostingList';

class AllPostings extends React.Component {
    componentDidMount() {
        document.title = "All Postings - Network";
    }

    render() {
        return (
            <div className="container mt-1 no-padding">
                <h2>All Postings</h2>
                <PostingList display_new_posting={true} />
            </div>
        );
    }
}

export default AllPostings
