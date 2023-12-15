import React, { useState, useEffect } from "react";
import Router from 'next/router';
import withAuth from '../../components/withAuthentication'


//The Patients component is used to display all patients in the database.
const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState('');
  
//The useEffect hook is used to fetch data from the API.
  useEffect(() => {
    fetch("https://api.kaspergaupmadsen.no/Patients/", {
      method: "GET",

      //The credentials: include is used to send the cookie with the request.
      credentials: "include",
    })
      
      //The response is checked to see if it is ok.
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })

      //The data is set to the patients state.
      .then((data) => {
        setPatients(data);
        setLoading(false);
      })

      //If there is an error, it is logged to the console.
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  }, []);

  //If the data is still loading, a spinner is displayed.
  if (loading) {
    return <div class="d-flex flex-column justify-content-center">
    <div class="spinner-border" role="status">
      <span class="sr-only">Loading...</span>
    </div>
  </div>;
  }

  //The handleRowClick function is used to redirect the user to the patient page when a row is clicked.
  const handleRowClick = (patientId) => {
    Router.push(`/home/patient/${patientId}`);
  };


  //The patients are displayed in a table. The table is styled using bootstrap. Maps through the patients array and displays the data in the table.
  return (
      <>
      <div className = "dashboardContainers">
      <h5>Patients List</h5>
      
      <table className = "table table-striped table-bordered table-dark table-sm table-hover w-50 p-3">
        <caption>List of all patients</caption>
        <thead className = "thead-dark">
          <tr>
            <th>ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Date of Birth</th>
          </tr>
        </thead>
        <tbody>
            {patients.map((patient) => (
              <tr key={patient.id} onClick={() => handleRowClick(patient.id)}>
                <td>{patient.id}</td>

                <td>{patient.first_name}</td>
                <td>{patient.last_name}</td>  
                <td>{patient.birthDate}</td>
              </tr>

            ))}
        </tbody>
      </table>
      </div>
    </>
    );
};

export default withAuth(Patients);
