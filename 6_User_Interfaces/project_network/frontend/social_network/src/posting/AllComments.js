import React from 'react';
import PropTypes from 'prop-types';
import MultilineContent from '../common/MultilineContent'
import UserLink from './UserLink'
import NewComment from './NewComment'

class AllComments extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // array containing objects with comment data
            comments_data: [],
            // number of comments that are available in the backend but are not yet inside comments_data
            num_comments_left: 0,
            no_comments_msg: null
        };
    }

    componentDidMount() {
        this.getComments();
    }

    // Get a certain number of comments for a posting.
    // do_clean:
    //  if False, append the new data to the existing comments data
    //  if True, create a new array from the received data
    getComments = (do_clean=false) => {
        // If new comment data shall be appended to the existing one,
        // specify the id of the last comment in the GET request to get the comments from that point.
        let last_comment_query = "";
        if (!do_clean && this.state.comments_data.length > 0) {
            let last_comment_id = this.state.comments_data[this.state.comments_data.length - 1].id;
            last_comment_query = `&last_comment=${last_comment_id}`;
        }

        fetch(`/api/comments?posting=${this.props.posting}${last_comment_query}`)
        .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
        .then(result => {
            if (!result.is_ok) {
                console.log(result.body.error);
                return
            }
            let extra_msg = null;
            if (result.body.comments.length === 0) {
                extra_msg = <div className="font-italic text-center my-2">No Comments.</div>
            }

            if (do_clean) {
                this.setState({comments_data: result.body.comments});
            } else {
                this.setState(state => ({
                    comments_data: [...state.comments_data, ...result.body.comments]
                }));
            }

            this.setState({
                no_comments_msg: extra_msg,
                num_comments_left: result.body.num_comments_queried - result.body.comments.length
            });
        })
        .catch((err) => {
            console.log(err);
        });
    }

    onCreate = () => {
        // reload posting data to show the new number of comments.
        this.props.updatePosting(this.props.posting);
        // Reload the comments to show the newly created comment.
        // Clear all previous loaded comments. Otherwise it would be complicated to append the
        // new comment data to the current one, in case there were comments created from others in the meantime.
        this.getComments(true);
    }

    render() {
        // if there are still comments available, display a button to load more
        let load_comments_btn = null;
        if (this.state.num_comments_left > 0) {
            load_comments_btn = 
            <div className="text-center">
                <button type="button" className="btn btn-link no-padding" onClick={() => this.getComments()}>
                    &#9662; Load more Comments ({this.state.num_comments_left} more)
                </button>
            </div>
        }
        return (
            <div>
            <NewComment posting={this.props.posting} onCreate={this.onCreate} />
            {this.state.no_comments_msg}
            {this.state.comments_data.map(comment_data =>
                <div key={comment_data.id.toString()} className="container my-2 mx-auto">
                    <UserLink user={comment_data.user} user_id={comment_data.user_id} />
                    <span className="timestamp ml-2">Created {comment_data.timestamp}</span>
                    <MultilineContent content={comment_data.content} />
                </div>
            )}
            {load_comments_btn}
            </div>
        );
    }
}

AllComments.propTypes = {
    posting: PropTypes.number.isRequired,
    updatePosting: PropTypes.func.isRequired,
};

export default AllComments
