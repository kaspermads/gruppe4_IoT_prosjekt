import React, { useEffect, useState } from 'react';
import Router from 'next/router';
import Layout from '../../components/layout';

import withAuth from '../../components/withAuthentication'


//CSRF token is used to prevent cross-site request forgery attacks.
function getCSRFToken() {
    const csrfToken = document.cookie.match(new RegExp('(^| )csrftoken=([^;]+)'));
    return csrfToken ? csrfToken[2] : null;
}


//The AddPatient component is used to display and handle the add patient form.
const AddPatient = () => {
    const [firstName, setfirstName] = useState('');
    const [lastName, setlastName] = useState('');
    const [birthDate, setBirthDate] = useState('');
    const [address, setAddress] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [error, setError] = useState('');


    const [csrfToken, setCsrfToken] = useState('');

    useEffect(() => {
        const token = getCSRFToken();
        if (token !== csrfToken) {
            setCsrfToken(token);
            }
        }, []); 

    //The handleSubmit function is used to handle the submit of the form.
    const handleSubmit = async (event) => {

        //The event is prevented from refreshing the page.
        event.preventDefault();
        const formattedBirthDate = birthDate.split('/').reverse().join('-');
        
        //The patient data is set to the patientData variable.
        const patientData = {
            first_name: firstName,
            last_name: lastName,
            birthDate: formattedBirthDate,
            address: address,
            phone: phoneNumber};

        // Perform the API call
        try {
            const response = await fetch('https://api.kaspergaupmadsen.no/api/register-patient/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {}),
                },

                //The patient data is sent to the API.
                body: JSON.stringify(patientData),
                credentials: 'include',
            });


            //If the response is ok, the user is redirected to the dashboard page.
            if (response.ok) {
                Router.push('/home/dashboard/');

            //If the response is not ok, an error message is displayed.
            } else {
                const errData = await response.json();
                setError(errData.detail || 'An error occurred while adding the patient.');
            }
            
        //If there is an error, it is logged to the console.
        } catch (error) {
            setError('An error occurred. Please try again.');
        }
    };

    //The form is displayed. The form is styled using bootstrap. The form is submitted when the submit button is clicked.
    //The data is sent to the handleSubmit function.
    return (
        <>
            <Layout>
            <h1>Register a new patient</h1>
            {error && <p className="error">Error: {error}</p>}
            <form onSubmit={handleSubmit}>
                <div className ="mb-3">
                    <label className = "form-label">First Name</label>
                    <input
                        type="text"
                        className = "form-control"
                        
                        value={firstName}
                        onChange={(e) => setfirstName(e.target.value)}
                        required
                    />
                </div>
                <div className ="mb-3">
                    <label className = "form-label">Last Name</label>
                    <input
                        type="text"
                        className = "form-control"
                        value={lastName}
                        onChange={(e) => setlastName(e.target.value)}
                        required
                    />
                </div>
                    <div className="mb-3">
                        <label className="form-label">Birthdate</label>
                        <input
                            type="date"
                            className="form-control"
                            value={birthDate}
                            onChange={(e) => setBirthDate(e.target.value)}
                            required    
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Address</label>
                        <input
                            type="text"
                            className="form-control"
                            value={address}
                            onChange={(e) => setAddress(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Phone Number</label>
                        <input
                            type="text"
                            className="form-control"
                            value={phoneNumber}
                            onChange={(e) => setPhoneNumber(e.target.value)}
                            required
                        />
                    </div>

                <button type="submit" className="btn btn-primary">Register</button>
                </form>
            </Layout>
        </>
    );
};

export default withAuth(AddPatient);
