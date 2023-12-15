import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import withAuth from '../../../components/withAuthentication';
import BloodPressureChart from '../../../components/charts';
import OxygenSaturationChart from '../../../components/o2_chart';


//The PatientDetail component is used to display the patient details page, which is when you click on a patient in the patients list.
const PatientDetail = () => {
  const [patient, setPatient] = useState(null);
  //const {bloodPressureData, setBloodPressureData} = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const { patientId } = router.query;


  //The useEffect hook is used to fetch data from the API.
  useEffect(() => {
    if (patientId) {
      //Fetch patient data
      fetch(`https://api.kaspergaupmadsen.no/Patients/${patientId}`, {
        method: "GET",
        credentials: "include",
      })

        //The response is checked to see if it is ok. If it is, the data is set to the patient state.
        .then((response) => response.json())
        .then((data) => {
          setPatient(data);
          setLoading(false);
        })

        //If there is an error, it is logged to the console.
        .catch((error) => {
          console.error("Error fetching patient data:", error);
          setLoading(false);
        });
    }
  }, [patientId]);


  //If the data is still loading, a spinner is displayed.
  if (loading) {
    return <div class="d-flex flex-column justify-content-center">
    <div class="spinner-border" role="status">
      <span class="sr-only">Loading...</span>
    </div>
  </div>;
  }

  //If there is no patient data, a message is displayed.
  if (!patient) {
    return <div>No patient data found.</div>;
  }

  //The patient details are displayed in a table. The table is styled using bootstrap.
  //Maps through the patient array and displays the data in the table.
  return (
    <>
      <div className = "dashboardContainers">
      <h3>Patient Details</h3>
      <table className="table table-dark table-striped table-bordered table-sm table-hover w-50 p-3">
        <tbody>
          <tr>
            <th id="overskrift">ID</th>
            <td>{patient.id}</td>
                      
          </tr>
          <tr>
            <th>First Name</th>
            <td>{patient.first_name}</td>
          </tr>
          <tr>
            <th>Last Name</th>
            <td>{patient.last_name}</td>
          </tr>
          <tr>
            <th>Address</th>
            <td>{patient.address}</td>
          </tr>
          <tr>
            <th>Phone Number</th>
            <td>{patient.phone}</td>
          </tr>
          <tr>
            <th>Date of Birth</th>
            <td>{patient.birthDate}</td>
          </tr>
          <tr>
            <th>Added by</th>
            <td>{patient.added_by}</td>
          </tr>
        </tbody>
        </table>
        </div>

      <div className = "dashboardContainers">
      <h3>Blood Pressure Data for {patient.first_name}</h3>
      {patient.patient_blood_pressure_data && patient.patient_blood_pressure_data.length > 0 ? (
        <table className="table custom-bp-table table-dark table-bordered table-striped table-sm w-50 p-3">
          <thead className = "thead-dark">
            <tr>
              <th>Date</th>
              <th>Systolic</th>
              <th>Diastolic</th>
              <th>Pulse</th>
            </tr>
          </thead>
          <tbody>
            {patient.patient_blood_pressure_data.map((record, index) => (
              <tr key={index}>
                <td>{record.timestamp}</td>
                <td>{record.systolic}</td>
                <td>{record.diastolic}</td>
                <td>{record.pulse}</td>
              </tr>
            ))}
          </tbody>
          </table>
      ) : (
        <div>No blood pressure data found.</div>
        
        
      )}
      </div>
      
      <div className="dashboardContainers">
        <h3>Oxygen Saturation data for {patient.first_name}</h3>
        {patient.patient_blood_oxygen_saturation_data && patient.patient_blood_oxygen_saturation_data.length > 0 ? (
          <table className="table custom-bp-table table-dark table-bordered table-striped table-sm w-50 p-3">
            <thead className = "thead-dark">
              <tr>
                <th>Date</th>
                <th>Saturation</th>
              </tr>
            </thead>
            <tbody>
              {patient.patient_blood_oxygen_saturation_data.map((record, index) => (
                <tr key={index}>
                  <td>{record.timestamp}</td>
                  <td>{record.oxygen_saturation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div>No oxygen saturation data found for the patient.</div>
        )}
      </div>


      <div className = "chartContainer">
        <BloodPressureChart patient_blood_pressure_data={patient.patient_blood_pressure_data} />
      </div>

      <div className="chartContainer">
        <OxygenSaturationChart patient_blood_oxygen_saturation_data={patient.patient_blood_oxygen_saturation_data} />
      </div>
    </>
  );
};

export default withAuth(PatientDetail);
