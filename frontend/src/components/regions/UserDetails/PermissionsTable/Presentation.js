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
                    Object.keys(permissionInstances).length > 0 ?
                        Object.keys(permissionInstances).map((key) => (
                            <TableRow key={key}>
                                <TableCell>{permissionInstances[key].name}</TableCell>
                                <TableCell>{permissionInstances[key].active ? 'True' : 'False'}</TableCell>
                                <TableCell>
                                    {permissionInstances[key].permissions.map((permissionsChip) => (
                                        <Chip key={permissionInstances[key].permissions.indexOf(permissionsChip)} className={classes.permissionsChip} label={permissionsChip} />
                                    ))}
                                </TableCell>
                            </TableRow>
                        )) :
                        <TableRow>
                            <TableCell colSpan='3'>Nothing to display</TableCell>
                        </TableRow>
                }
            </TableBody>
        </Table>
    )
}

PermissionsTable.propTypes = {
    permissionInstances: PropTypes.object,
}

export default PermissionsTable;