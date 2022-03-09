import React from 'react'
import { rest } from 'msw'
import { setupServer } from 'msw/node'
import { render, fireEvent, waitFor, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import RegistrationForm from '../components/RegistrationForm'

const server = setupServer(
  rest.get('/register', (req, res, ctx) => {
    return res(ctx.json({
      'error': 'invalid submission',
      'detail': {
        'username': [{ string: 'This field is required.', code: 'required' }],
        'first_name': [{ string: 'This field is required.', code: 'required' }],
        'last_name': [{ string: 'This field is required.', code: 'required' }],
        'email': [{ string: 'This field is required.', code: 'required' }],
        'password': [{ string: 'This field is required.', code: 'required' }],
        'password_confirmation': [{ string: 'This field is required.', code: 'required' }]
      }
    }))
  })
)

// beforeAll(() => server.listen())
// afterEach(() => server.resetHandlers())
// afterAll(() => server.close())
//
// test('displays errors from invalid registration attempt', async () => {
//   render(<RegistrationForm url="/register" />)
//
//   fireEvent.click(screen.getByText('Load Greeting'))
//
//   await waitFor(() => screen.getByRole('heading'))
//
//   expect(screen.getByRole('heading')).toHaveTextContent('hello there')
//   expect(screen.getByRole('button')).toBeDisabled()
// })