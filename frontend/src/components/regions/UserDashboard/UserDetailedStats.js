import React from "react";

import {
  Table,
  TableBody,
  TableCell,
  TableRow,
  Typography,
} from "@material-ui/core";

import { PieChart, Pie, Cell, Tooltip } from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

const renderCustomizedLabel = ({ cardStatusPieData }) => {
  return ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
    console.log({
      cx,
      cy,
      midAngle,
      innerRadius,
      outerRadius,
      percent,
      index,
    });
    const RADIAN = Math.PI / 180;

    const radius = outerRadius + (outerRadius - innerRadius) * 0.5;
    // const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="black"
        textAnchor={x > cx ? "start" : "end"}
        dominantBaseline="central"
      >
        {cardStatusPieData[index].name}
      </text>
    );
  };
};

export default ({ detailedStats }) => {
  if (!detailedStats) return <React.Fragment />;
  
  const cardsAssignedWithStatusComplete = detailedStats.cardsAssignedWithStatusComplete;
  const cardsAssignedWithStatusInReview = detailedStats.cardsAssignedWithStatusInReview;
  const cardsAssignedWithStatusReviewFeedback = detailedStats.cardsAssignedWithStatusReviewFeedback;
  const cardsAssignedWithStatusInProgress = detailedStats.cardsAssignedWithStatusInProgress;

  const cardStatusPieData = [
    { name: `Complete (${cardsAssignedWithStatusComplete})`, value: cardsAssignedWithStatusComplete },
    { name: `Review (${cardsAssignedWithStatusInReview})`, value: cardsAssignedWithStatusInReview },
    {
      name: `Review Feedback (${cardsAssignedWithStatusReviewFeedback})`,
      value: cardsAssignedWithStatusReviewFeedback,
    },
    {
      name: `In Progress (${cardsAssignedWithStatusInProgress})`,
      value: cardsAssignedWithStatusInProgress,
    },
  ].filter((element) => element.value);
  return (
    <React.Fragment>
      <Typography variant="h6" component="h2">
        Assigned card statuses
      </Typography>
      <PieChart width={600} height={400}>
        <Pie
          data={cardStatusPieData}
          dataKey="value"
          cx="50%"
          cy="50%"
          innerRadius={20}
          outerRadius={90}
          label={renderCustomizedLabel({ cardStatusPieData })}
        >
          {cardStatusPieData.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={COLORS[index % COLORS.length]}
            ></Cell>
          ))}
        </Pie>
        <Tooltip />
      </PieChart>

      <Table>
        <TableBody>
          <TableRow>
            <TableCell>
              <Typography variant="h6" component="h2">
                Performance
              </Typography>
            </TableCell>
          </TableRow>

          <TableRow>
            <TableCell>Cards completed in the last 7 days</TableCell>
            <TableCell>
              {detailedStats.cardsCompletedLast_7DaysAsAssignee}
            </TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Cards started in the last 7 days as assignee</TableCell>
            <TableCell>
              {detailedStats.cardsStartedLast_7DaysAsAssignee}
            </TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Total competence reviews done</TableCell>
            <TableCell>{detailedStats.totalTildeReviewsDone}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Total competence reviews done in last 7 days</TableCell>
            <TableCell>{detailedStats.tildeReviewsDoneLast_7Days}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Total pull request reviews done</TableCell>
            <TableCell>{detailedStats.totalPrReviewsDone}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Total pull request reviews done in last 7 day</TableCell>
            <TableCell>{detailedStats.prReviewsDoneLast_7Days}</TableCell>
          </TableRow>
          <TableRow>
            <TableCell>Tilde cards reviewed in last 7 days</TableCell>
            <TableCell>
              {detailedStats.tildeCardsReviewedInLast_7Days}
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </React.Fragment>
  );
};
