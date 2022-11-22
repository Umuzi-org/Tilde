import { createTheme } from "@material-ui/core/styles";

const theme = createTheme({
  overrides: {
    MuiTooltip: {
      tooltip: {
        fontSize: "1em",
        backgroundColor: "#f5f5f9",
        color: "rgba(0, 0, 0, 0.87)",
        maxWidth: 220,
        border: "1px solid #dadde9",
      },
    },
  },
});

export default theme;
