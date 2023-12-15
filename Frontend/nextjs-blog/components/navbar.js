import Head from 'next/head';

import { AuthContext } from './AuthContext';
import { useContext } from 'react';
import Link from 'next/link';


import Router from "next/router";


export default function Layout({ children, showNavbar = true }) {
  const { isAuthenticated, logout } = useContext(AuthContext);

  const handleLogout = async (e) => {
    e.preventDefault();
    logout();
  };

  return (
    <>
      <Head>
        <title>Patient Portal</title>
      </Head>
      <nav className="navbar navbar-expand-lg bg-body-tertiary">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            Patient Portal
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNavDropdown"
            aria-controls="navbarNavDropdown"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNavDropdown">
            <ul className="navbar-nav">
              <li className="nav-item">
                <a
                  className="nav-link active"
                  aria-current="page"
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    Router.push("/home/patients-test");
                  }}
                >
                  Patients
                </a>
              </li>
              <li className="nav-item">
                <a
                  className="nav-link"
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    Router.push("/home/add-patient");
                  }}
                >
                  Add Patient
                </a>
              </li>

              {isAuthenticated && (
                <li className="nav-item">
                  <a className="nav-link" href="#" onClick={handleLogout}>
                    Logout
                  </a>
                </li>
              )}
            </ul>
          </div>
        </div>
      </nav>
      <main>{children}</main>
    </>
  );

}
