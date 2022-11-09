import { createTheme } from '@material-ui/core/styles';

const ToolTipTheme = createTheme({
    overrides: {
        MuiTooltip: {
            tooltip: {
                fontSize: "1em",
            },
        },
    },
});

export default ToolTipTheme;