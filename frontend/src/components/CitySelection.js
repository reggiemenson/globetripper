import React, { useState, useEffect } from 'react'
import Select from 'react-select'
import makeAnimated from 'react-select/animated'
import axios from 'axios'
import Auth from '../lib/Auth'
import {
  Accordion,
  AccordionItem,
  AccordionItemHeading,
  AccordionItemButton,
  AccordionItemPanel
} from 'react-accessible-accordion'

import { toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'




const CitySelection = (props) => {

  const notify = () => toast('Successfully Changed Cities!' ,{
    progressClassName: 'toast-progress'
  })

  const [towns, setTowns] = useState([])
  const [errors, setErrors] = useState('')
  const [searchBar, setSearchBar] = useState('')
  // const [townsVisited, setTownsVisited] = useState([])
  const [user, setUser] = useState({})
  const [data, setData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    towns: []
  })



  function getTownData() {
    axios.get('/api/towns/')
      .then(resp => {
        // console.log('Response!')
        setTowns(resp.data)
      })
      .catch(err => setErrors(err.response.message))
  }

  function getUserData() {
    axios.get('/api/profile', {
      headers: { Authorization: `Bearer ${Auth.getToken()}` }
    })
      .then(resp => {
        // console.log('Response!')
        const town_ids = resp.data.towns.map(town => town.id.toString())
        setData({
          username: resp.data.username,
          first_name: resp.data.first_name,
          last_name: resp.data.last_name,
          towns: town_ids
        })
        setUser(resp.data)
      })
      .catch(err => {
        console.log(err)
        setErrors(err)
      })
  }

  useEffect(() => {
    getTownData()
    getUserData()
  }, [])

  function handleSearchChange(e) {
    setSearchBar(e.target.value)
  }

  function filterBySearch(towns) {
    return towns.filter(town => {
      if (searchBar !== '') return town.name.toLowerCase().includes(searchBar.toLowerCase()) || town.country.toLowerCase().includes(searchBar.toLowerCase())
      return town
    })
  }

  function handleCheck(e) {
    // console.log(e.target.checked)
    // console.log(e.target.id)

    if (e.target.checked) {
      const towns = [...data.towns]
      towns.push(e.target.id)
      setData({ ...data, towns })

    } else {
      const towns = [...data.towns]
        .filter(id => id !== e.target.id)
      setData({ ...data, towns })
    }
  }

  function handleSubmit(e) {
    e.preventDefault()
    axios.put('/api/profile/edit/all', data, {
      headers: { Authorization: `Bearer ${Auth.getToken()}` }
    })
      .then(resp => {
        // console.log(resp.data)
        notify()
        props.history.push(`/profile/${resp.data.id}`)
      })
      .catch(err => {
        setErrors(err)
        console.log(err)
      })
    return
  }

  return (
    <section className="section" id="city-selection">
      <div className="container">
        {/* {console.log(data)} */}
        <h1 className="title">Select cities</h1>
        <h2 className="subtitle">Where have you travelled to?</h2>

        <form className="form" onSubmit={handleSubmit}>
          <div className="columns is-mobile">
            <div className="column is-10-desktop is-8-tablet is-8-mobile">
              <div className="field">
                <div className="control has-icons-left">
                  <input className="input has-text-info" type="search" placeholder="Search for countries or cities" onChange={handleSearchChange}></input>
                  <span className="icon is-small is-left">
                    <i className="fas fa-compass"></i>
                  </span>
                </div>
              </div>
            </div>

            <div className="column column is-2-desktop is-4-tablet is-4-mobile has-text-right">
              <button className="button is-link" id="send-request">
                Done
              </button>
            </div>

          </div>
        </form>


        {towns.length === 0 ? <div className="loading">Loading cities...</div> : <></>}
        <Accordion
          allowMultipleExpanded={true}
          allowZeroExpanded={true}
        >
          {towns &&
            [...new Set(filterBySearch(towns).map(town => town.country))]
              .sort()
              .map((country, i) => {

                return <AccordionItem key={i}>
                  <AccordionItemHeading>
                    <AccordionItemButton>
                      <p className="is-size-6">
                        {country}
                      </p>
                    </AccordionItemButton>
                  </AccordionItemHeading>
                  <AccordionItemPanel>
                    {filterBySearch(towns)
                      .filter(town => town.country === country)
                      .sort(function (a, b) {
                        if (a.name < b.name) { return -1 }
                        if (a.name > b.name) { return 1 }
                        return 0
                      })
                      .map((town, i) => {
                        return <div key={i} className="field">
                          <input
                            className="is-checkradio is-info"
                            id={town.id}
                            type="checkbox"
                            name={town.id}
                            onChange={handleCheck}
                            checked={data.towns.includes(town.id.toString()) ? true : false}
                          />
                          <label className="city-checkbox-label" htmlFor={town.id}>{town.name} ({town.admin_name})</label>
                        </div>

                      })
                    }
                  </AccordionItemPanel>
                </AccordionItem>

              })
          }


        </Accordion>
      </div>
    </section>
  )
}

export default CitySelection



