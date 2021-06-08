import React from 'react';
import PropTypes from 'prop-types';

const ReviewTrustTable = ({ title, flavours }) => {
    return (
        <table className='table'>
            <tr>
                <th className='titleColumn'>Title</th>
                <th className='flavoursColumn'>Flavours</th>
            </tr>
            <tr>
                <td>{title}</td>
                <td>{flavours}</td>
            </tr>
        </table>
    )
}

ReviewTrustTable.propTypes = {
    title: PropTypes.string,
    flavours: PropTypes.array
}

export default ReviewTrustTable;
