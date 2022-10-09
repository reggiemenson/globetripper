import React from 'react'
import { rest } from 'msw'
import { render, fireEvent, screen } from '@testing-library/react'
import { server } from '../mocks/server'

import RegistrationForm from '../components/RegistrationForm'

test('displays errors from invalid registration attempt', async () => {
    render(<RegistrationForm url="/register" />)

    server.resetHandlers(
        rest.post('/api/register', (req, res, ctx) => {
            return res(
                ctx.status(422),
                ctx.json({
                    detail: {
                        username: ['This field is required.'],
                        first_name: ['This field is required.'],
                        last_name: ['This field is required.'],
                        email: ['This field is required.'],
                        password: ['This field is required.'],
                        password_confirmation: ['This field is required.'],
                    },
                })
            )
        })
    )

    fireEvent.click(screen.getByText('Register'))

    const helpText = await screen.findAllByRole('help-text')

    expect(helpText).toHaveLength(6)
})

// test('displays errors from invalid registration attempt', async () => {
//     render(<RegistrationForm url="/register"/>)

//     server.resetHandlers(
//         rest.post('/api/register', (req, res, ctx) => {
//             return res(
//                 ctx.status(422),
//                 ctx.json({
//                     'username': ['This field is required.'],
//                     'first_name': ['This field is required.'],
//                     'last_name': ['This field is required.'],
//                     'email': ['This field is required.'],
//                     'password': ['This field is required.'],
//                     'password_confirmation': ['This field is required.']
//                 }))
//         })
//     )

//     fireEvent.click(screen.getByText('Register'))

//     const helpText = await waitFor(() => screen.getAllByRole('help-text'))

//     expect(helpText).toHaveLength(6)
// })
