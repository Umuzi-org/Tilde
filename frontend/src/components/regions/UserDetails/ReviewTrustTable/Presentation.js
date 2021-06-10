import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Chip from '@material-ui/core/Chip';

const columns = [
    { id: 'title', label: 'Title', minWidth: 170 },
    { id: 'flavours', label: 'Flavours', minWidth: 100 }
];

const useStyles = makeStyles({

    flavourChip: {
        marginRight: '0.5rem',
    },
});

let haveTrustInstances = (arr) => {
    return arr.length > 0;
}

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
                    haveTrustInstances(trustInstances) ? 
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
                        <TableRow></TableRow> 
                }
            </TableBody>
        </Table>
    )
}

ReviewTrustTable.propTypes = {
    trustInstances: PropTypes.array
}

export default ReviewTrustTable;
