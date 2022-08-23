import React, { useRef } from "react";
import Button from "@material-ui/core/Button";
// import UploadButton from "./UploadButton";

export default function ProfilePicture() {
  const uploadedImage = useRef(null);
  const imageUploader = useRef(null);

  const handleImageUpload = (event) => {
    const [file] = event.target.files;
    if (file) {
      const reader = new FileReader();
      const { current } = uploadedImage;
      current.file = file;
      reader.onload = (e) => {
        current.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div
      style={{
        position: "relative",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justfyContent: "center",
      }}
    >
      <input
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        ref={imageUploader}
        style={{ display: "none", height: "100%", width: "100%" }}
      />
      <div style={{ position: "relative" }}>
        <Button
          style={{
            position: "absolute",
            bottom: 0,
            height: "100%",
            width: "100%",
            border: "1px solid red",
          }}
          onClick={() => imageUploader.current.click()}
        >
          <img
            ref={uploadedImage}
            style={{
              position: "relative",
              width: "15em",
              height: "15em",
            }}
          />
          Upload
        </Button>
      </div>
    </div>
  );
}
