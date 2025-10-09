import React, { useEffect, useState } from "react";
import api from "../api.js";
import AddDataForm from "./AddDataForm";

const DataResponseList = () => {
  const [dataResponse, setDataResponse] = useState([]);

  const fetchDataResponse = async () => {
    try {
      const response = await api.get("/dataResponse");
      setDataResponse(response.data.data);
    } catch (error) {
      console.error("Error fetching data", error);
    }
  };

  const addData = async (dataName) => {
    try {
      await api.post("/dataResponse", { name: dataName });
      fetchDataResponse(); // Refresh the list after adding data
    } catch (error) {
      console.error("Error adding data", error);
    }
  };

  useEffect(() => {
    fetchDataResponse();
  }, []);

  return (
    <div>
      <h2>Data Response List</h2>
      <ul>
        {dataResponse.map((data, index) => (
          <li key={index}>{data.name}</li>
        ))}
      </ul>
      <AddDataForm addData={addData} />
    </div>
  );
};

export default DataResponseList;
