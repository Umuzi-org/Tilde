import React, { useState } from "react";

export default function ChangeNickName({ name, onChange, onClick }) {
  const [isEditing, setIsEditing] = useState(false);

  const handleClick = () => {
    setIsEditing(true);
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      setIsEditing(false);
    }
  };

  console.log("test", handleClick)

  return (
    <React.Fragment>
      {isEditing ? (
        <input
          autoFocus
          value={name}
          onChange={onChange}
          onKeyPress={handleKeyPress}
          type="text"
          // style={{display: "inline-block";
          //   border: "1px solid #ccc";}}
        />
      ) : (
        <span onClick={handleClick}>{name}</span>
      )}
    </React.Fragment>
  );
}
