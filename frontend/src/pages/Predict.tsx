import { useState } from 'react'
import type { FormEvent } from 'react'
import axios from 'axios'
import api from '../api'

const categories = [
  'Electronics', 'Books', 'Jewelry', 'Toys', 'Skincare', 'Snacks', 'Outdoors', 'Apparel',
  'Sports', 'Grocery', 'Pet Supplies', 'Home', 'Cosmetics', 'Kitchen', 'Clothing', 'Shoes',
]

interface Result {
  id: number
  predicted_minutes: number
  estimated_arrival: string
  model_version: string
  note: string
}

function nowLocal() {
  const d = new Date()
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  return d.toISOString().slice(0, 16)
}

function formatDuration(minutes: number) {
  const hours = Math.floor(minutes / 60)
  const mins = Math.round(minutes % 60)
  return hours > 0 ? `${hours} h ${mins} min` : `${mins} min`
}

const inputClass = 'w-full border border-slate-300 rounded-lg px-3 py-2 bg-white'

export default function Predict() {
  const [form, setForm] = useState({
    agent_age: '30',
    agent_rating: '4.5',
    weather: 'Sunny',
    traffic: 'Low',
    vehicle: 'motorcycle',
    area: 'Urban',
    category: 'Electronics',
    distance_km: '5',
    departure_time: nowLocal(),
  })
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function update(name: string, value: string) {
    setForm({ ...form, [name]: value })
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setResult(null)
    setLoading(true)
    try {
      const res = await api.post('/api/v1/predictions', {
        ...form,
        agent_age: Number(form.agent_age),
        agent_rating: Number(form.agent_rating),
        distance_km: Number(form.distance_km),
      })
      setResult(res.data)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 422) {
        setError('Some values are not valid. Please check the form.')
      } else {
        setError('Could not get a prediction. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold text-slate-800">New Prediction</h2>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow p-6 grid gap-4 sm:grid-cols-2">
        <label className="text-sm text-slate-600">
          Distance (km, up to 25)
          <input type="number" required min="0.1" max="25" step="0.1" value={form.distance_km}
            onChange={(e) => update('distance_km', e.target.value)} className={inputClass} />
        </label>
        <label className="text-sm text-slate-600">
          Departure date and time
          <input type="datetime-local" required value={form.departure_time}
            onChange={(e) => update('departure_time', e.target.value)} className={inputClass} />
        </label>
        <label className="text-sm text-slate-600">
          Vehicle
          <select value={form.vehicle} onChange={(e) => update('vehicle', e.target.value)} className={inputClass}>
            <option value="motorcycle">Motorcycle</option>
            <option value="scooter">Scooter</option>
            <option value="van">Van</option>
          </select>
        </label>
        <label className="text-sm text-slate-600">
          Traffic
          <select value={form.traffic} onChange={(e) => update('traffic', e.target.value)} className={inputClass}>
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
            <option>Jam</option>
          </select>
        </label>
        <label className="text-sm text-slate-600">
          Weather
          <select value={form.weather} onChange={(e) => update('weather', e.target.value)} className={inputClass}>
            <option>Sunny</option>
            <option>Cloudy</option>
            <option>Fog</option>
            <option>Stormy</option>
            <option>Sandstorms</option>
            <option>Windy</option>
          </select>
        </label>
        <label className="text-sm text-slate-600">
          Area
          <select value={form.area} onChange={(e) => update('area', e.target.value)} className={inputClass}>
            <option>Metropolitan</option>
            <option>Urban</option>
            <option>Semi-Urban</option>
            <option>Other</option>
          </select>
        </label>
        <label className="text-sm text-slate-600">
          Item category
          <select value={form.category} onChange={(e) => update('category', e.target.value)} className={inputClass}>
            {categories.map((c) => <option key={c}>{c}</option>)}
          </select>
        </label>
        <label className="text-sm text-slate-600">
          Delivery agent age (15 to 50)
          <input type="number" required min="15" max="50" value={form.agent_age}
            onChange={(e) => update('agent_age', e.target.value)} className={inputClass} />
        </label>
        <label className="text-sm text-slate-600">
          Delivery agent rating (1 to 5)
          <input type="number" required min="1" max="5" step="0.1" value={form.agent_rating}
            onChange={(e) => update('agent_rating', e.target.value)} className={inputClass} />
        </label>
        <div className="sm:col-span-2">
          <button type="submit" disabled={loading}
            className="w-full bg-blue-600 text-white rounded-lg py-2 font-medium hover:bg-blue-700 disabled:opacity-50">
            {loading ? 'Predicting...' : 'Predict Delivery Time'}
          </button>
        </div>
      </form>

      {error && <p className="bg-red-50 text-red-600 rounded-lg p-3">{error}</p>}

      {result && (
        <div className="bg-white rounded-xl shadow p-6 space-y-3">
          <p className="text-sm text-slate-500">Predicted delivery time</p>
          <p className="text-4xl font-bold text-blue-600">{formatDuration(result.predicted_minutes)}</p>
          <p className="text-slate-700">
            Estimated arrival: {new Date(result.estimated_arrival).toLocaleString()}
          </p>
          <p className="text-sm text-slate-500">
            Reference ID: {result.id} | Model version: {result.model_version}
          </p>
          <p className="text-sm bg-amber-50 text-amber-700 rounded-lg p-3">{result.note}</p>
        </div>
      )}
    </div>
  )
}