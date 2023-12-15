import { useContext, useState } from "react";
import { AuthContext }  from "../../components/AuthContext";
import Router from "next/router";
import LayoutLogin  from "../../components/layout";


//The Login component is used to display and handle the login form.
const Login = () => {
  const { login } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // The handleSubmit function is used to handle the submit of the form.
  const handleSubmit = async (event) => {
    event.preventDefault();

    // Calls the API to login
    // Perform the API call and check response
    try {
      const response = await fetch(
        "https://api.kaspergaupmadsen.no/api/login/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, password }),

          //
          credentials: "include",
        }
      );

      if (response.ok) {
        login();
        // Redirect to the dashboard or homepage after login
        Router.push("/home/dashboard/");
      } else {
        setError("Invalid username or password");
      }
    } catch (error) {
      setError("An error occurred. Please try again.");
    }
  };

  //Notice that the entire form is wrapped in LayoutLogin. 
  //This is because the login page should not have the same layout as the rest of the pages.
  //The login page should not have the navigation bar for example.
  return (
    <>
      <LayoutLogin>
        <h1>Login</h1>
        {error && <p className="error">Error: {error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Username</label>
            <input
              type="username"
              className="form-control"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary">
            Login
          </button>
        </form>
      </LayoutLogin>
    </>
  );
};

export default Login;
