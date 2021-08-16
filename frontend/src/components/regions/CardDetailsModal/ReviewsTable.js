import React, { useState } from "react";
import MUIDataTable from "mui-datatables";
import Chip from "@material-ui/core/Chip";
import CheckCircleIcon from '@material-ui/icons/CheckCircle';

const ReviewsTable = () => {
  const [responsive] = useState("vertical");
  const [tableBodyHeight] = useState("100%");
  const [tableBodyMaxHeight] = useState("");

  const timestamp = Date.now();

  const columns = [
    {
      name: "timestamp",
      label: "Timestamp",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "status",
      label: "Status",
      options: {
        filter: true,
        sort: false,
      },
    },
    {
      name: "reviewer",
      label: "Reviewer",
      options: {
        filter: true,
        sort: false,
      },
    },
    {
      name: "comments",
      label: "Comments",
      options: {
        filter: true,
        sort: false,
      },
    },
    {
      name: "badge",
      options: {
        filter: true,
        sort: false,
        empty: true,
        customBodyRender: (value, tableMeta, updateValue) => {
          return (<CheckCircleIcon />)
        },
      },
    },
  ];

  const options = {
    elevation: 6,
    filter: false,
    filterType: "dropdown",
    search: false,
    viewColumns: false,
    selectTableRows: "none",
    download: false,
    confirmFilters: false,
    print: false,
    selectableRows: false,
    customToolbarSelect: () => {},
    responsive,
    tableBodyHeight,
    tableBodyMaxHeight,
  };

  const data = [
    {
      timestamp: new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }).format(timestamp),
      status: <Chip variant="outlined" size="small" label="Excellent" />,
      reviewer: "sheena.oconnel@umuzi.org",
      comments:
        "This has to be lOnHgf Aadf ADFH ADJKADFH ADF DAJKADFH JHADFADF JKHA KHADF KJH AJK FFHADFHJADFH KADFHJKHFJA HA DADFAKJF KJAHADFJADFH KADFHJKADFHADJKH ADFKHADF HH ADFK ADHKjhsjkHhKHkjhLHjkHHjkjklh ajksh h as jasghj hasg gh gjklh",
    },
    {
      timestamp: new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }).format(timestamp),
      status: <Chip variant="outlined" size="small" label="Competent" />,
      reviewer: "sbonelo.mkhize@umuzi.org",
      comments: "Nicely done",
    },
    {
      timestamp: new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }).format(timestamp),
      status: <Chip variant="outlined" size="small" label="Not Yet Competent" />,
      reviewer: "babalwa.mbolekwa@umuzi.org",
      comments: "Good work",
    },
    {
      timestamp: new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      }).format(timestamp),
      status: <Chip variant="outlined" size="small" label="Red Flag" />,
      reviewer: "kaleem.mohammad@umuzi.org",
      comments: "What is this",
    },
  ];

  return (
    <React.Fragment>
      <MUIDataTable
        title={"Reviews"}
        data={data}
        columns={columns}
        options={options}
      />
    </React.Fragment>
  );
};

export default ReviewsTable;