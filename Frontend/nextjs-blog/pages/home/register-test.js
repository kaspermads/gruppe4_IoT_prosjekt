// pages/register.js
import React, { useState } from 'react';
import LayoutLogin from '../../components/layout';
import Router from 'next/router';


const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password1, setPassword1] = useState('');
    const [password2, setPassword2] = useState('');
    const [error, setError] = useState('');
    const [isRegistered, setIsRegistered] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Perform the API call
        try {
            const response = await fetch('https://api.kaspergaupmadsen.no/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password1, password2 }),
            });

            const data = await response.json();

            if (response.ok) {
                setIsRegistered(true);
                // Redirect or further processing
            } else {
                throw new Error(data.error || 'Registration failed.');
            }
        } catch (error) {
            setError(error.message);
        }
    };

    if (isRegistered) {
        Router.push('/home/login');
    }

    return (
        <>
            <LayoutLogin>
            <h1>Register</h1>
                {error && <p>Error: {error}</p>}
            
            <form className = "row g-3" onSubmit={handleSubmit}>
                <div className="col-md-6">
                    <label className="form-label">Username</label>
                    <input
                        type="text"
                        className="form-control"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="col-md-6">
                    <label className="form-label">Email</label>
                    <input
                        type="email"
                        className="form-control"
                        placeholder='example@mail.com'
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div className="col-md-6">
                    <label className="form-label">Password</label>
                    <input
                        type="password"
                        className="form-control"
                        aria-describedby='passwordHelpBlock'
                        value={password1}
                        onChange={(e) => setPassword1(e.target.value)}
                        required
                    />
                    <small id='passwordHelpBlock' className='form-text'>
                        Your password must be 8-20 characters long, contain letters and numbers, and at least one uppercase character.
                    </small>
                </div>
                <div className="col-md-6">
                    <label className="form-label">Confirm Password</label>
                    <input
                        type="password"
                        className="form-control"
                        value={password2}
                        onChange={(e) => setPassword2(e.target.value)}
                        required
                    />
                </div>
                <button className="btn btn-primary" type="submit">Register</button>
                </form>
                </LayoutLogin>
            
        </>
    );
};

export default Register;
