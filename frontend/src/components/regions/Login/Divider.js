// import React from "react";
// import { makeStyles } from "@material-ui/core";

// const useStyles = makeStyles(theme => ({
// 	container:{
// 		display: "flex",
// 		alignItems: "center",
// 	},
// 	border: {
// 		borderBottom: "2px solid lightgray",
// 		flexGrow: 1,
// 	},
// 	content: {
// 		paddingTop: theme.spacing(0.5),
// 		paddingBottom: theme.spacing(0.5),
// 		paddingRight: theme.spacing(2),
// 		paddingLeft: theme.spacing(2),
// 		fontWeight: 500,
// 		fontSize: 22,
// 		color: "lightgray",
// 	}
// }));

// const TextDivider = ({ children }) => {
// 	const classes = useStyles()
// 	return (
// 		<div className={classes.container}>
// 			<div className={classes.border} />
// 			<span className={classes.content}>{children}</span>
// 			<div className={classes.border} />
// 		</div>
// 	);
// };

// export default TextDivider;

import React from "react";
import {Grid, Divider as MuiDivider} from "@material-ui/core";

const Divider = ({children, ...props}) => (
	<Grid container alignItems="center" spacing={3} {...props}>
		<Grid item xs>
			<MuiDivider />
		</Grid>
		<Grid item>{children}</Grid>
		<Grid item xs>
			<MuiDivider />
		</Grid>
	</Grid>
	)

export default Divider;











