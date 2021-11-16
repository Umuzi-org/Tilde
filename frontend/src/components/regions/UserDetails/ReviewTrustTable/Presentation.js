import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Chip from '@mui/material/Chip';

const columns = [
    { id: 'title', label: 'Title', minWidth: 170 },
    { id: 'flavours', label: 'Flavours', minWidth: 100 }
];

const useStyles = makeStyles({

    flavourChip: {
        marginRight: '0.5rem',
    },
});

const ReviewTrustTable = (props) => {

    const { trustInstances } = props;
    const classes = useStyles();

    return (
        <Table stickyHeader aria-label="sticky table">
            <TableHead>
                <TableRow>
                    {columns.map((column) => (
                        <TableCell
                            key={column.id}
                            align={column.align}
                            style={{ minWidth: column.minWidth }}
                        >
                            {column.label}
                        </TableCell>
                    ))}
                </TableRow>
            </TableHead>
            <TableBody>
                {   
                    trustInstances ? 
                        trustInstances.map((trustInstance) => (
                            <TableRow>
                                <TableCell>{trustInstance.content_item_title}</TableCell>
                                <TableCell>
                                    {trustInstance.flavours.map((flavourChip) => (
                                        <Chip className={classes.flavourChip} label={flavourChip} />
                                    ))}
                                </TableCell>
                            </TableRow>
                        )) :
                        <TableRow>
                            <TableCell colSpan="2">Nothing to display</TableCell>
                        </TableRow> 
                }
            </TableBody>
        </Table>
    )
}

ReviewTrustTable.propTypes = {
    trustInstances: PropTypes.array
}

export default ReviewTrustTable;
