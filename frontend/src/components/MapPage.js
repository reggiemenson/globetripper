import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Auth from '../lib/Auth'

import WorldMap from './Worldmap'

const MapPage = () => {

  const [userData, setUserData] = useState({})
  const [platformData, setPlatformData] = useState({})
  const [errors, setErrors] = useState('')
  const [infoLevel, setInfoLevel] = useState('platform')

  function fetchTownData() {
    axios.get('/api/towns')
      .then(resp => {
        // console.log('RESPONSE')
        computePlatformData(resp.data)
        computeUserData(resp.data)
      })
      .catch(err => {
        console.log(err)
        setErrors({ ...errors, ...err })
      })
  }

  function computePlatformData(towns) {
    // console.log('computing platform country data...')
    const data = towns
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
    setPlatformData(uniqueVisitors)
  }

  function computeUserData(towns) {
    // console.log('computing user country data...')
    const data = towns
      .filter((town) => {
        return town.visitors.includes(Auth.getUserId())
      })
      .reduce((countries, town) => {
        if (countries[town.iso2]) {
          countries[town.iso2] += 1
        } else {
          countries[town.iso2] = 1
        }
        return countries
      }, {})
    setUserData(data)
  }

  useEffect(() => {
    fetchTownData()
  }, [])

  function toggleInfoLevel(e) {
    e.preventDefault()
    if (infoLevel !== e.target.id) {
      setInfoLevel(e.target.id)
    } 
  }

  function displayText(country) {
    let allcountriesdata = []
    if (infoLevel === 'platform') {
      allcountriesdata = platformData
    } else {
      allcountriesdata = userData
    }

    const num = allcountriesdata[country]

    if (infoLevel === 'platform') {
      if (num > 1) {
        return `${num} visitors`
      } else if (num === 1){
        return `${num} visitor`
      } else {
        return 'unexplored'
      }
    } else if (infoLevel === 'user') {
      if (num > 1) {
        return `${num} cities visited`
      } else if (num === 1) {
        return `${num} city visited`
      } else {
        return 'no city visited'
      }
    } else {
      return 'something went wrong'
    }
  }
  
  return (
    <section id="mappage" className="hero is-fullheight">
      {/* {console.log(infoLevel)} */}
      <div className="hero-body">

        <div className="columns is-desktop">
          <div className="column is-8-desktop">
            <div id="home-worldmap" className="has-text-centered is-centered">
              < WorldMap countriesData={infoLevel === 'platform' ? platformData : userData} displayText={displayText} />
            </div>
          </div>

          <div className="column is-4-desktop" id="title-column-mappage">
            <div className="container has-text-centered">
              {infoLevel === 'platform' ? <h1 className="title is-size-1 is-size-3-mobile">Where everybody&apos;s been</h1> : <></>}
              {infoLevel === 'user' ? <h1 className="title is-size-1 is-size-3-mobile">Where you&apos;ve been</h1> : <></>}
              <h2 className="is-size-4 is-size-5-mobile">
                Select an option below.
              </h2>
              <button id="platform" className={infoLevel === 'platform' ? 'button mappage is-link' : 'is-outlined button mappage is-link'} onClick={toggleInfoLevel}>Everybody&apos;s travels</button>
              <button id="user" className={infoLevel === 'user' ? 'button mappage is-link' : 'is-outlined button mappage is-link'} onClick={toggleInfoLevel}>Your travels</button>
            </div>
          
          </div>
        </div>

      </div>
    </section>
  )
}

export default MapPage