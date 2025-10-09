import React, { useState } from "react";

const AddDataForm = ({ addData }) => {
  const [dataName, setDataName] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    if (dataName) {
      addData(dataName);
      setDataName("");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={dataName}
        onChange={(e) => setDataName(e.target.value)}
        placeholder="Enter data name"
      />
      <button type="submit">Add Data</button>
    </form>
  );
};

export default AddDataForm;
