import React, {useState} from "react";
import ChangeNickName from "./NickNameChange"

export default function NickName() {
  const [nickName, setNickName] = useState([
    {
     name: "nick_name"
    }
  ]);

  const handleChange = (event, index) => {
    const value = event.target.value;
    setNickName(state => [
      ...state.slice(0, index),
      { ...state[index], name: value },
      ...state.slice(index + 1)
    ])
  }

  return (
    <div>
      {nickName.map((element, index) => {
        return(
          <ChangeNickName 
           name={element.name}
           onChange={e => handleChange(e, index)}
           />
        );
      })}
    </div>
  )
}
