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
    { id: 'name', label: 'Team Name', minWidth: 170 },
    { id: 'active', label: 'Active', minWidth: 100 },
    { id: 'permissions', label: 'Permissions', minWidth: 100 },
];

const useStyles = makeStyles({

    permissionsChip: {
        marginRight: '0.3rem',
        marginBottom: '0.3rem',
    },
});

const PermissionsTable = (props) => {

    const { permissionInstances } = props;
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
                    Object.keys(permissionInstances.teams).map((key, value) => (
                        <TableRow>
                            <TableCell>{permissionInstances.teams[key].name}</TableCell>
                            <TableCell>{permissionInstances.teams[key].active ? 'True' : 'False'}</TableCell>
                            <TableCell>
                                {permissionInstances.teams[key].permissions.map((permissionsChip) => (
                                    <Chip className={classes.permissionsChip} label={permissionsChip} />
                                ))}
                            </TableCell>
                        </TableRow>
                    ))
                }
            </TableBody>
        </Table>
    )
}

PermissionsTable.propTypes = {
    permissionInstances: PropTypes.object,
}

export default PermissionsTable;