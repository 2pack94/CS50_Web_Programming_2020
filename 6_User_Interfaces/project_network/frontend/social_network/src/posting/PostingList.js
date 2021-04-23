import React from 'react';
import PropTypes from 'prop-types';
import { withRouter } from "react-router";
import Pagination from '../common/Pagination';
import Posting from './Posting';
import NewPosting from './NewPosting';

class PostingList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // array containing objects with posting data
            postings_data: [],
            no_postings_msg: null,
            // current page number in the pagination
            page_number: 0,
            // total number of pages in the pagination
            num_pages: 0
        };

        // This component uses pagination to display the postings.
        // The current page is determined by the value of the 'page' key in the query string of the URL.
        let search_param = new URLSearchParams(this.props.location.search);
        this.search_param_page = search_param.get("page");

        // This variable is used to save and restore the y scroll position
        this.scroll_y = null;
    }

    componentDidMount() {
        this.getPostings();
    }

    componentDidUpdate() {
        this.restoreScrollPos();

        // When a link is clicked (All Postings in the navigation bar or page in the Pagination)
        // this component gets re-rendered.
        // getPostings should not get called immediately after clicking a page link (with onClick),
        // because the new search parameter in the URL is not available yet.
        // getPostings will be triggered when the value of 'page' in the URL query string changes.
        // If 'page' is not present, this.search_param_page will be null.
        // The actual page number is determined by the backend response.
        let search_param_page_prev = this.search_param_page;
        let search_param = new URLSearchParams(this.props.location.search);
        this.search_param_page = search_param.get("page");

        if (this.search_param_page !== search_param_page_prev) {
            this.getPostings();
        }
    }

    saveScrollPos = () => {
        this.scroll_y = window.scrollY;
    }

    restoreScrollPos = () => {
        if (this.scroll_y !== null) {
            window.scrollTo(0, this.scroll_y);
            this.scroll_y = null;
        }
    }

    // Get the data of all postings on the current page.
    getPostings = () => {
        // this.search_param_page is always updated before calling this function.
        let querystring = `page=${this.search_param_page}`
        if (this.props.user) {
            // only get postings of a specific user
            querystring += `&user=${this.props.user}`
        } else if (this.props.following) {
            // only get postings of users that are followed
            querystring += `&following=${this.props.following}`
        }

        // key/ value pairs after the '?' will be available as GET parameters in the backend.
        fetch(`/api/postings?${querystring}`)
        .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
        .then(result => {
            if (!result.is_ok) {
                console.log(result.body.error);
                return
            }
            let extra_msg = null;
            if (result.body.postings.length === 0) {
                extra_msg =
                <div className="font-italic text-center my-2">
                    No Postings available.
                </div>
            }

            this.setState({
                postings_data: result.body.postings,
                no_postings_msg: extra_msg,
                page_number: result.body.page,
                num_pages: result.body.num_pages
            });
        })
        .catch((err) => {
            console.log(err);
        });
    }

    // retrieve the data to update a single posting.
    updatePosting = (id) => {
        fetch(`/api/posting/${id}`)
        .then(response => response.json().then(data => ({is_ok: response.ok, body: data})))
        .then(result => {
            if (!result.is_ok) {
                console.log(result.body.error);
                return
            }
            // Updating the data of a posting triggers a re-render.
            // Save the scroll position to restore it after rendering.
            this.saveScrollPos();

            // Find the posting object to update in the array.
            // shallow copy
            let postings_data = this.state.postings_data;
            for (let i = 0; i < postings_data.length; i++) { 
                if (postings_data[i].id === id) {
                    postings_data[i] = result.body;
                    break;
                }
            }
            this.setState({postings_data});
        })
        .catch((err) => {
            console.log(err);
        });
    }

    render() {
        return (
            <div>
            {this.props.display_new_posting && this.state.page_number === 1 &&
                <NewPosting onCreate={this.getPostings} />
            }
            {this.state.no_postings_msg}
            {this.state.postings_data.map(posting_data =>
                <Posting key={posting_data.id.toString()} data={posting_data}
                    updatePosting={this.updatePosting} />
            )}
            <Pagination
                page_number={this.state.page_number}
                num_pages={this.state.num_pages}
                link_dest={this.props.location.pathname} />
            </div>
        );
    }
}

PostingList.defaultProps = {
    display_new_posting: false
};

PostingList.propTypes = {
    // if only postings of a specific user should be displayed, specify the user id
    user: PropTypes.number,
    // if true, only postings of followed users are displayed
    following: PropTypes.bool,
    // if true, display the form to create a new posting
    display_new_posting: PropTypes.bool
};

// withRouter passes match, location, and history props to the component
export default withRouter(PostingList)
