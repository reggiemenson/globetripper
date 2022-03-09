import React from 'react'
import { rest } from 'msw'
import { setupServer } from 'msw/node'
import { render, fireEvent, waitFor, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import RegistrationForm from '../components/RegistrationForm'

const server = setupServer(
    rest.post('/api/register', (req, res, ctx) => {
        return res(
            ctx.status(422),
            ctx.json({
                'username': ['This field is required.'],
                'first_name': ['This field is required.'],
                'last_name': ['This field is required.'],
                'email': ['This field is required.'],
                'password': ['This field is required.'],
                'password_confirmation': ['This field is required.']
            }))
    })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

test('displays errors from invalid registration attempt', async () => {
    render(<RegistrationForm url="/register"/>)

    fireEvent.click(screen.getByText('Register'))

    await waitFor(() => screen.getAllByRole('help-text'))

    expect(screen.getAllByRole('help-text')).toHaveLength(6)
})
