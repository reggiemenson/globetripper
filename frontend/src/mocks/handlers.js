import { rest } from 'msw'


export const handlers = [
    rest.post('/api/register', (req, res, ctx) => {
        return res(
            ctx.status(200),
            ctx.json({
                'detail': 'Registration successful'
            }))
    }),
    rest.post('/api/login', (req, res, ctx) => {
        return res(
            ctx.status(200),
            ctx.json({
                'detail': 'Welcome Amanda!',
                'token': 'a long, totally legit token'
            }))
    })
]