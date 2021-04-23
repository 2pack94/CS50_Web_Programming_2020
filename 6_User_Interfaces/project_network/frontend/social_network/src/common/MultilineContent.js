import React from 'react';
import PropTypes from 'prop-types';

// Loop over each line and put it inside <p> Tags.
// The <br> is necessary for line breaks in case a line has no content.
class MultilineContent extends React.Component {
    render() {
        return (
            <div>
            {this.props.content.split("\n").map((line, line_i) =>
                <p key={line_i} className="content-paragraph text-break">
                    {line}<br />
                </p>
            )}
            </div>
        );
    }
}

MultilineContent.propTypes = {
    content: PropTypes.string.isRequired
};

export default MultilineContent
