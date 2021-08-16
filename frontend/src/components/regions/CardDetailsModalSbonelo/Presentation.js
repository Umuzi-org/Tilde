import React, { useState } from "react";
// import ReactDOM from "react-dom";
import MUIDataTable from "mui-datatables";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";

const ReviewsTable = () => {
  const [responsive, setResponsive] = useState("vertical");
  const [tableBodyHeight, setTableBodyHeight] = useState("400px");
  const [tableBodyMaxHeight, setTableBodyMaxHeight] = useState("");

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
    filter: true,
    filterType: "dropdown",
    responsive,
    tableBodyHeight,
    tableBodyMaxHeight,
  };

  const date = new Date();

  const data = [
    {
      timestamp: `${date.getDate()}`,
      status: "Excellent",
      reviewer: "sheena.oconnel@umuzi.org",
      comments:
        "This has to be lOnHgf Aadf ADFH ADJKADFH ADF DAJKADFH JHADFADF JKHA KHADF KJH AJK FFHADFHJADFH KADFHJKHFJA HA DADFAKJF KJAHADFJADFH KADFHJKADFHADJKH ADFKHADF HH ADFK ADHKjhsjkHhKHkjhLHjkHHjkjklh ajksh h as jasghj hasg gh gjklh",
    },
    {
      timestamp: `${date.getDate()}`,
      status: "Competent",
      reviewer: "sbonelo.mkhize@umuzi.org",
      comments: "Nicely done",
    },
    {
      timestamp: `${date.getDate()}`,
      status: "Not Yet Competent",
      reviewer: "babalwa.mbolekwa@umuzi.org",
      comments: "Good work",
    },
    {
      timestamp: `${date.getDate()}`,
      status: "Red Flag",
      reviewer: "kaleem.mohammad@umuzi.org",
      comments: "What is this",
    },
  ];

  return (
    <React.Fragment>
      <FormControl>
        <InputLabel id="demo-simple-select-label">Choose Device</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={responsive}
          style={{ width: "200px", marginBottom: "10px", marginRight: 10 }}
          onChange={(e) => setResponsive(e.target.value)}
        >
          <MenuItem value={"vertical"}>vertical</MenuItem>
          <MenuItem value={"standard"}>standard</MenuItem>
          <MenuItem value={"simple"}>simple</MenuItem>

          <MenuItem value={"scroll"}>scroll (deprecated)</MenuItem>
          <MenuItem value={"scrollMaxHeight"}>
            scrollMaxHeight (deprecated)
          </MenuItem>
          <MenuItem value={"stacked"}>stacked (deprecated)</MenuItem>
        </Select>
      </FormControl>
      <FormControl>
        <InputLabel id="demo-simple-select-label">Table Body Height</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={tableBodyHeight}
          style={{ width: "200px", marginBottom: "10px", marginRight: 10 }}
          onChange={(e) => setTableBodyHeight(e.target.value)}
        >
          <MenuItem value={""}>[blank]</MenuItem>
          <MenuItem value={"400px"}>400px</MenuItem>
          <MenuItem value={"800px"}>800px</MenuItem>
          <MenuItem value={"100%"}>100%</MenuItem>
        </Select>
      </FormControl>
      <MUIDataTable
        title={"Reviews"}
        data={data}
        columns={columns}
        options={options}
      />
    </React.Fragment>
  );
}

export default ReviewsTable

// ReactDOM.render(<App />, document.getElementById("root"));
