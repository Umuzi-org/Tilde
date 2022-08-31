import React, { useState } from "react";
import ChangeNickName from "./NickNameChange";
import EditTwoToneIcon from '@material-ui/icons/EditTwoTone';

export default function NickName() {
  const [nickName, setNickName] = useState([
    {
      name: "nick_name",
    },
  ]);

  const handleChange = (event, index) => {
    const value = event.target.value;
    setNickName((state) => [
      ...state.slice(0, index),
      { ...state[index], name: value },
      ...state.slice(index + 1),
    ]);
  };

  return (
    <div>
      {nickName.map((element, index) => {
        return (
          <div style={{position: "relative"}}>
          <ChangeNickName
            name={element.name}
            onChange={(e) => handleChange(e, index)}
          />
            <EditTwoToneIcon fontSize="small" style={{paddingLeft: "20px", paddingTop: "14px"}} />
          </div>
        );
      })}
    </div>
  );
}
