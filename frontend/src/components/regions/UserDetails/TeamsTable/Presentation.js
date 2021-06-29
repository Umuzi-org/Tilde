import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

const columns = [
    { id: 'number', label: 'ID', minWidth: 170 },
    { id: 'teams', label: 'Team', minWidth: 100 },
];

const useStyles = makeStyles({

    teamsChip: {
        marginRight: '0.3rem',
        marginBottom: '0.3rem',
    },
});

const TeamsTable = (props) => {

    const { teams } = props;
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
                    Object.keys(teams).length > 0 ?
                        Array.from(teams).map((team) => (
                            <TableRow key={Array.from(teams).indexOf(team)}>
                                <TableCell>{Array.from(teams).indexOf(team)}</TableCell>
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