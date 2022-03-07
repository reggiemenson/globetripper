import React from 'react'
import { Route, Redirect } from 'react-router-dom'
import Auth from './Auth'

// Create a secure route you can only see when logged in
const SecureRoute = (props) => {
  if (Auth.isAuthorized()) return <Route {...props} />
  return <Redirect to="/" />
}

export default SecureRoute