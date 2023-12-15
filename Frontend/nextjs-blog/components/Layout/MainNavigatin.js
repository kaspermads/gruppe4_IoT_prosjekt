import { useContext } from "react";
import Link from "next/link";
import { AuthContext } from "../AuthContext";

import classes from "../../styles/MainNavigation.module.css";
import "bootstrap/dist/css/bootstrap.min.css";



export default function MainNavigation({children, showNav = true}) {
    const { isAuthenticated, logout } = useContext(AuthContext);

    const logoutHandler = async (e) => {
        e.preventDefault();
        logout();
    };

    return (

        <>
        {showNav && (
        <header className={classes.header}>
            <div className={classes.logo}><Link href = "/home/patients-test"><a>Gruppe 4 Helsetjeneste</a></Link></div>
            <nav>
                <ul>
                    <li>
                        <Link href="/home/patients-test">
                            <a>Patients</a>
                        </Link>
                    </li>
                    <li>
                        <Link href="/home/add-patient">
                            <a>Add New Patient</a>
                        </Link>
                    </li>
                    {isAuthenticated && (
                    <li className={classes.actions}>
                        <button onClick={logoutHandler}>Logout</button>
                    </li>
                    )}
                </ul>
            </nav>
        </header>
        )}
        <main>{children}</main>

        </>
    );
}
