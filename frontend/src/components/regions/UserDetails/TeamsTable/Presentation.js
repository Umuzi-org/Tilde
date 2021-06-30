import React from 'react';
import PropTypes from 'prop-types';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

const columns = [
    { id: 'id', label: 'ID', minWidth: 60 },
    { id: 'teams', label: 'Team', minWidth: 100 },
];

const TeamsTable = (props) => {

    const { teams } = props;

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
                    Object.keys(teams).length > 0 ?
                        Object.values(teams).map((team) => (
                            <TableRow key={Object.values(teams).indexOf(team)}>
                                <TableCell>{Object.values(teams).indexOf(team) + 1}</TableCell>
                                <TableCell>
                                    {team.name}
                                </TableCell>
                            </TableRow>
                        )) :
                        <TableRow>
                            <TableCell colSpan='2'>Nothing to display</TableCell>
                        </TableRow>
                }
            </TableBody>
        </Table>
    )
}

TeamsTable.propTypes = {
    teams: PropTypes.object,
}

export default TeamsTable;