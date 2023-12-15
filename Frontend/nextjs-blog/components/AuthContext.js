import Router  from 'next/router';
import React, { createContext, useState, useEffect } from 'react';
import { useRouter } from 'next/router';



export const AuthContext = createContext({

    isAuthenticated: false,
    isLoading: true,
    login: () => {},
    logout: () => { }
});

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();


    useEffect(() => {
        if (
        router.pathname !== '/' && 
        router.pathname !== '/home/login' && 
        router.pathname !== '/home/register-test')
        {
            const verifyToken = async () => {
                try {
                    // Replace '/api/verify' with your API endpoint that checks for authentication
                    const response = await fetch('https://api.kaspergaupmadsen.no/api/token/verify/', {
                        method: 'POST',
                        credentials: 'include' // Needed to include the HttpOnly cookie in the request
                    });
          
                    if (response.ok) {
                        setIsAuthenticated(true);
                    } else {
                        setIsAuthenticated(false);
                        Router.push('/');
                    }
                } catch (error) {
                    setIsAuthenticated(false);
                    Router.push('/');
                }
        
                setIsLoading(false);
            };

            verifyToken();
        }
    }, [router.pathname]);



  

    const logout = async () => {
        try {
            const response = await fetch('https://api.kaspergaupmadsen.no/api/logout/', {
            //const response = await fetch('http://localhost:8000/api/logout/', {
                method: 'POST',
                credentials: 'include'
            });

            if (response.ok) {
                setIsAuthenticated(false);
                Router.push('/');
            } else {
                console.error('Logout failed');
            }
        } catch (error) {
            console.error('Logout failed', error);
        }
    };
    const login = () => {
        setIsAuthenticated(true);
    };
    
        

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
  
};
