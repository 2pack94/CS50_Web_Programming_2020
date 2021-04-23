import React from 'react';
import PropTypes from 'prop-types';
import { Link } from "react-router-dom";

// Pagination styling: https://getbootstrap.com/docs/4.6/components/pagination/
// When a Page link is clicked, the page number is appended to the url as a querystring.
// The parent component can then read this querystring.

class Pagination extends React.Component {
    render() {
        // specifies how many pages should be displayed to the left and to the right of the current page (if present).
        const show_num_pages_lr = 2;
        // list of page numbers that shall be displayed in the pagination.
        let page_number_list = [];
        for (let i = this.props.page_number - show_num_pages_lr; i <= this.props.page_number + show_num_pages_lr; i++) {
            if (i >= 1 && i <= this.props.num_pages) {
                page_number_list.push(i);
            }
        }
        let previous_page_number = Math.max(1, this.props.page_number - 1);
        let next_page_number = Math.min(this.props.num_pages, this.props.page_number + 1);

        let disable_left = this.props.page_number <= 1 ? "disabled" : "";
        let disable_right = this.props.page_number >= this.props.num_pages ? "disabled" : "";

        return (
            <nav aria-label="Page navigation">
                <ul className="pagination justify-content-center">
                    <li className={`page-item ${disable_left}`}>
                        <Link to={{
                            pathname: this.props.link_dest, search: `?page=${1}`}}
                            className="page-link" onClick={window.scrollTo(0, 0)}
                        >
                            &laquo;
                        </Link>
                    </li>
                    <li className={`page-item ${disable_left}`}>
                        <Link to={{
                            pathname: this.props.link_dest, search: `?page=${previous_page_number}`}}
                            className="page-link" onClick={window.scrollTo(0, 0)}
                        >
                            &lsaquo;
                        </Link>
                    </li>
                    {page_number_list.map(page_num => {
                        let active_page = page_num === this.props.page_number ? "active" : "";
                        return (
                            <li key={page_num.toString()} className={`page-item ${active_page}`}>
                                <Link to={{
                                    pathname: this.props.link_dest, search: `?page=${page_num}`}}
                                    className="page-link" onClick={window.scrollTo(0, 0)}
                                >
                                    {page_num}
                                </Link>
                            </li>
                        )
                    })}
                    <li className={`page-item ${disable_right}`}>
                        <Link to={{
                            pathname: this.props.link_dest, search: `?page=${next_page_number}`}}
                            className="page-link" onClick={window.scrollTo(0, 0)}
                        >
                            &rsaquo;
                        </Link>
                    </li>
                    <li className={`page-item ${disable_right}`}>
                        <Link to={{
                            pathname: this.props.link_dest, search: `?page=${this.props.num_pages}`}}
                            className="page-link" onClick={window.scrollTo(0, 0)}
                        >
                            &raquo;
                        </Link>
                    </li>
                </ul>
            </nav>
        )
    }
}

Pagination.propTypes = {
    page_number: PropTypes.number.isRequired,
    num_pages: PropTypes.number.isRequired,
    // base url that is navigated to when a link is clicked.
    link_dest: PropTypes.string.isRequired
};

export default Pagination
