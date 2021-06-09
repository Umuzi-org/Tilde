import React from 'react';
import PropTypes from 'prop-types';

const ReviewTrustTable = (props) => {

    const { title, flavours } = props;

    
    return (
        <table className='table'>
            <tr>
                <th className='titleColumn'>Title</th>
                <th className='flavoursColumn'>Flavours</th>
            </tr>
            <tr>
                <td>{title}</td>
                <td>
                    <ul>
                        {flavours.split(",").map((flavour) => <li>{flavour}</li>)}
                    </ul>
                </td>
            </tr>
        </table>
    )
}

ReviewTrustTable.propTypes = {
    title: PropTypes.string,
    flavours: PropTypes.string
}

export default ReviewTrustTable;
