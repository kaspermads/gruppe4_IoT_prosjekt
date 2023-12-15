import React, { useState, useContext } from "react";
import Patients from "./patients-test";
import AddPatient from "./add-patient";
import { AuthContext } from "../../components/AuthContext";
import withAuth from "../../components/withAuthentication";


//The Dashboard component is used to display the dashboard page.
function Dashboard() {
  const [activePage, setActivePage] = useState("patients");
  const { isAuthenticated } = useContext(AuthContext);

  //We use the DashboardContent function to display the correct page based on the activePage state.
  const DashboardContent = () => {
    switch (activePage) {
      case "patients":
        return <Patients />;
      case "add-patient":
        return <AddPatient />;
      default:
        return <Patients />;
    }
  };

  //If the user is not authenticated, a spinner is displayed while the user is being authenticated or redirected to the login page.
  return isAuthenticated ? <main>{DashboardContent()}</main> : <div class="d-flex justify-content-center">
  <div class="spinner-border" role="status">
    <span class="sr-only">Loading...</span>
  </div>
</div>
}
export default withAuth(Dashboard);
