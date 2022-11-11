import { createTheme } from '@material-ui/core/styles';

const theme = createTheme({
    overrides: {
        MuiTooltip: {
            tooltip: {
                fontSize: "1em",
            },
        },
    },
});

export default theme;