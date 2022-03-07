import React from 'react'

const Settings = ({ data, errors, handleChange, modalSubmit }) => {

  return <>
    <div className='container has-text-centered'>
      <div className='columns'>
        <div className='column'>
          <form className='form has-text-centered' onSubmit={modalSubmit}>

            <div className='field'>
              <div className='control has-icons-left has-icons-right'>
                <input
                  onChange={handleChange}
                  type='text'
                  name='username'
                  className='input has-text-info'
                  value={data.username}
                />
                <span className='icon is-small is-left'>
                  <i className='fas fa-user'></i>
                </span>
                {/* <span className='icon is-small is-right'>
                  <i className='fas fa-check'></i>
                </span> */}
              </div>
            </div>
            {errors.username && <small className='help is-danger'>
              {errors.username[0]}
            </small>}
            <div className='field'>
              <p className='control has-icons-left'>
                <input
                  onChange={handleChange}
                  className='input has-text-info'
                  type='text'
                  name='first_name'
                  value={data.first_name}
                />
                <span className='icon is-small is-left'>
                  <i className='fas fa-id-card'></i>
                </span>
              </p>
            </div>
            {errors.first_name && <small className='help is-danger'>
              {errors.first_name[0]}
            </small>}
            <div className='field'>
              <p className='control has-icons-left'>
                <input
                  onChange={handleChange}
                  className='input has-text-info'
                  type='text'
                  name='last_name'
                  value={data.last_name}
                />
                <span className='icon is-small is-left'>
                  <i className='fas fa-id-card'></i>
                </span>
              </p>
            </div>
            {errors.last_name && <small className='help is-danger'>
              {errors.last_name[0]}
            </small>}
            <div className="field">
              <div className="control">
                <div className='control has-icons-left'>
                  <div className='select is-link'>
                    <select
                      onChange={handleChange}
                      value={data.dexterity}
                      name='dexterity'>
                      <option value='RH'>Right-handed operation</option>
                      <option value='LH'>Left-handed operation</option>
                    </select>
                  </div>
                  <span className="icon is-small is-left">
                    <i className='fas fa-gamepad'></i>
                  </span>
                </div>
              </div>
            </div>

            <button className='button is-link'>
              Save
            </button>
          </form>
        </div>
      </div>
    </div>

  </>
}

export default Settings