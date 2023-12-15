import { AuthProvider } from "../components/AuthContext";
import "bootstrap/dist/css/bootstrap.min.css";

import "../styles/global.css";
import MainNavigation from "../components/Layout/MainNavigatin";
import { useRouter } from "next/router";
import { useEffect } from "react";



export default function App({ Component, pageProps }) {
  const router = useRouter();
  const showNav = router.pathname !== "/" && 
                  router.pathname !== "/home/login" && 
                  router.pathname !== "/home/register-test";
  useEffect(() => {
    require("bootstrap/dist/js/bootstrap.bundle.min.js");
  }, []);

  return (
    <AuthProvider>
      <div className = "dark-mode">
      <MainNavigation showNav={showNav}>
        <Component {...pageProps} />
      </MainNavigation>
      </div>
    </AuthProvider>
  );
}
