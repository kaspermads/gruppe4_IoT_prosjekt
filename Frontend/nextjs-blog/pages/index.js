import Head from 'next/head';

import styles from '../styles/Home.module.css';




export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Patient Portal</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1 className={styles.title}>
          Patient Portal
        </h1>

        <p className={styles.description}>
          Get started by logging in or registering
        </p>

        <div className={styles.grid}>
          <a href="/home/register-test" className={styles.card}>
            <h3>Register &rarr;</h3>
            <p>Register with your information to gain access.</p>
          </a>

          <a href="/home/login" className={styles.card}>
            <h3>Login &rarr;</h3>
            <p>Login in to access the portal and view patients.</p>
          </a>

          
         
        </div>
      </main>

      <footer>
        <p>
          Made by group 4
        </p>
      </footer>
    </div>
    );
    
  
}
