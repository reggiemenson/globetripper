import '@testing-library/jest-dom'
import { server } from './frontend/src/mocks/server'

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())