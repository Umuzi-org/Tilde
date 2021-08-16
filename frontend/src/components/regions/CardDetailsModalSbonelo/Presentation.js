import React, { useState } from "react";
// import ReactDOM from "react-dom";
import MUIDataTable, {TableFilterList} from "mui-datatables";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import { CardBadges } from "../../widgets/CardBadges";
import Chip from "@material-ui/core/Chip";
import TagFacesIcon from '@material-ui/icons/TagFaces';
import { makeStyles } from '@material-ui/core/styles';

const ReviewsTable = () => {
  const [responsive, setResponsive] = useState("vertical");
  const [tableBodyHeight, setTableBodyHeight] = useState("100%");
  const [tableBodyMaxHeight, setTableBodyMaxHeight] = useState("");

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
    // checkboxSelection,
    responsive,
    tableBodyHeight,
    tableBodyMaxHeight,
  };

  const data = [
    {
      timestamp: new Intl.DateTimeFormat('en-US', {year: 'numeric', month: '2-digit',day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit'}).format(timestamp),
      status: "Excellent",
      reviewer: "sheena.oconnel@umuzi.org",
      comments:
        "This has to be lOnHgf Aadf ADFH ADJKADFH ADF DAJKADFH JHADFADF JKHA KHADF KJH AJK FFHADFHJADFH KADFHJKHFJA HA DADFAKJF KJAHADFJADFH KADFHJKADFHADJKH ADFKHADF HH ADFK ADHKjhsjkHhKHkjhLHjkHHjkjklh ajksh h as jasghj hasg gh gjklh",
    },
    {
      timestamp: new Intl.DateTimeFormat('en-US', {year: 'numeric', month: '2-digit',day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit'}).format(timestamp),
      status: "Competent",
      reviewer: "sbonelo.mkhize@umuzi.org",
      comments: "Nicely done",
    },
    {
      timestamp: new Intl.DateTimeFormat('en-US', {year: 'numeric', month: '2-digit',day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit'}).format(timestamp),
      status: "Not Yet Competent",
      reviewer: "babalwa.mbolekwa@umuzi.org",
      comments: "Good work",
    },
    {
      timestamp: new Intl.DateTimeFormat('en-US', {year: 'numeric', month: '2-digit',day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit'}).format(timestamp),
      status: "Red Flag",
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
