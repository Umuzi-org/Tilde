import React from 'react';

function Presentation(props) {
    const { variant = 'primary', children, ...rest } = props;
    return (
        <div>
            Hello world
        </div>
    )
}

export default Presentation;
