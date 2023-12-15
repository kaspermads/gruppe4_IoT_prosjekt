// withAuth.js
import { useContext, useEffect } from 'react';
import { AuthContext } from './AuthContext';
import Router from 'next/router';

const withAuth = (WrappedComponent) => {
  return (props) => {
    const { isAuthenticated, isLoading } = useContext(AuthContext);

    useEffect(() => {
      if (!isLoading && !isAuthenticated) {
        Router.push('/home/login');
      }
    }, [isAuthenticated, isLoading]);

    if (isLoading) {
      return <div class="d-flex justify-content-center">
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>;
    }

    return <WrappedComponent {...props} />;
  };
};

export default withAuth;
