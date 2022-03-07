import React, { useState, useEffect } from 'react'
import axios from 'axios'

import Register from './RegistrationForm'
import Login from './LoginForm'
import WorldMap from './Worldmap'
import Auth from '../lib/Auth'

// const infoType = 'user'

const Hero = (props) => {

  const [registrationModal, setRegistrationModal] = useState(false)
  const [loginModal, setLoginModal] = useState(false)
  const [countriesData, setCountriesData] = useState({})
  const [errors, setErrors] = useState('')

  function fetchTownData() {
    axios.get('/api/towns')
      .then(resp => {
        // console.log('RESPONSE')
        const data = resp.data
          .reduce((countries, town) => {
            if (countries[town.iso2]) {
              countries[town.iso2] = countries[town.iso2].concat(town.visitors)
            } else {
              countries[town.iso2] = town.visitors
            }
            return countries
          }, {})
        const uniqueVisitors = {}
        Object.keys(data).forEach((country) => {
          uniqueVisitors[country] = (new Set(data[country])).size
        })
        setCountriesData(uniqueVisitors)
      })
      .catch(err => {
        console.log(err)
        alert(err)
        setErrors({ ...errors, ...err })
      })
  }

  useEffect(() => {
    fetchTownData()
  }, [])


  function toggleRegistration() {
    setRegistrationModal(!registrationModal)
  }

  function toggleLogin() {
    setLoginModal(!loginModal)
  }

  useEffect(() => {
    const listener = e => {
      if (e.key === 'Escape') {
        setRegistrationModal(false)
        setLoginModal(false)
      }
    }
    window.addEventListener('keydown', listener)
  }, [])

  function displayText(country) {
    const num = countriesData[country]
    if (num > 1) {
      return `${num} visitors`
    } else if (num === 1){
      return `${num} visitor`
    } else {
      return 'unexplored'
    }
  }

  return (
    <section id="homepage" className="hero is-fullheight">
      <div className="hero-body">
        <div className="columns is-desktop">
          <div className="column is-8-desktop">
            <div id="home-worldmap" className="has-text-centered is-centered">
              <WorldMap displayText={displayText} countriesData={countriesData} />
            </div>
          </div>

          <div className="column is-4-desktop" id="title-column">
            <div className="container has-text-centered">
              <h1 className="title is-size-1">
                TripBit
              </h1>
              <h2 className="subtitle is-size-4">
                Your Personal Travel Tracker
              </h2>
              {!Auth.isAuthorized() && <div>
                <button className="is-size-4 homepage" onClick={toggleLogin}>Login</button>
                <button className="is-size-4 homepage" onClick={toggleRegistration}>Register</button>
              </div>}
            </div>
          </div>
        </div>

      </div>


      <div className={registrationModal === true ? 'modal is-active' : 'modal'}>
        <div className="modal-background" onClick={toggleRegistration}></div>
        <div className="modal-content">
          <Register
            toggleRegistration={toggleRegistration}
            toggleLogin={toggleLogin}
          />
        </div>
        <button className="modal-close is-large" aria-label="close" onClick={toggleRegistration}></button>
      </div>
      <div className={loginModal === true ? 'modal is-active' : 'modal'}>
        <div className="modal-background" onClick={toggleLogin}></div>
        <div className="modal-content">
          <Login props={props} />
        </div>
        <button className="modal-close is-large" aria-label="close" onClick={toggleLogin}></button>
      </div>
    </section>
  )
}

export default Hero