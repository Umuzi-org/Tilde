import React from "react";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";
import { Link } from "react-router-dom";
import MoreIcon from "@material-ui/icons/More";
import { routes } from "../../../routes";
import Button from "../../widgets/Button";
import UserAvatarLink from "../../widgets/UserAvatarLink";

const useStyles = makeStyles((theme) => ({
  dateTypography: {
    marginTop: theme.spacing(2),
    fontSize: 25,
  },
  title: { fontWeight: "bold" },
  event: { padding: theme.spacing(1), marginTop: theme.spacing(1) },
  flex: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
}));

function EventEntry({ item }) {
  const classes = useStyles();
  return (
    <Paper
      className={classes.event}
      timestamp={item.timestamp}
      style={{ borderLeft: `5px solid ${item.eventColor}` }}
      variant="outlined"
    >
      <div className={classes.flex}>
        <Typography>
          {item.eventName.split("_").join(" ").toUpperCase()}
        </Typography>

        <Typography>
          {new Date(item.timestamp).toTimeString().substring(0, 8)}
        </Typography>
      </div>

      <Typography className={classes.title}>
        {item.object1Summary.title}
      </Typography>
      <div className={classes.flex}>
        {item.actorUserEmail && (
          <UserAvatarLink email={item.actorUserEmail} userId={item.actorUser} />
        )}
        <Link
          to={routes.cardDetails.route.path.replace(
            ":cardId",
            item.object1Summary.card
          )}
        >
          <Button label="" startIcon={<MoreIcon />} variant="text" />{" "}
        </Link>
      </div>
    </Paper>
  );
}

export default function ActivityLog({ eventList, orderedDates }) {
  const classes = useStyles();
  return (
    <>
      {orderedDates.map((timestamp) => (
        <>
          <Typography variant="h3" className={classes.dateTypography}>
            {new Date(timestamp.substring(0, 10)).toDateString()}
          </Typography>

          {eventList.map((item) => (
            <>
              {item.timestamp.substring(0, 10) ===
                timestamp.substring(0, 10) && (
                <EventEntry item={item} key={item.id} />
              )}
            </>
          ))}
        </>
      ))}
    </>
  );
}
