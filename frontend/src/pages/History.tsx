import { useEffect, useState } from 'react'
import api from '../api'

interface Prediction {
  id: number
  weather: string
  traffic: string
  vehicle: string
  area: string
  category: string
  distance_km: number
  predicted_minutes: number
  created_at: string
}

const selectClass = 'border border-slate-300 rounded-lg px-3 py-2 bg-white text-sm'

export default function History() {
  const [items, setItems] = useState<Prediction[]>([])
  const [search, setSearch] = useState('')
  const [vehicle, setVehicle] = useState('All')
  const [traffic, setTraffic] = useState('All')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/api/v1/predictions')
      .then((res) => setItems(res.data))
      .catch(() => setError('Could not load the history. Please try again.'))
      .finally(() => setLoading(false))
  }, [])

  const text = search.trim().toLowerCase()

  const shown = items.filter((item) => {
    if (vehicle !== 'All' && item.vehicle !== vehicle) return false
    if (traffic !== 'All' && item.traffic !== traffic) return false
    if (!text) return true
    return (
      String(item.id) === text ||
      item.category.toLowerCase().includes(text) ||
      item.area.toLowerCase().includes(text) ||
      item.weather.toLowerCase().includes(text)
    )
  })

  if (loading) return <p className="text-slate-500">Loading...</p>
  if (error) return <p className="bg-red-50 text-red-600 rounded-lg p-3">{error}</p>

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold text-slate-800">Delivery History</h2>

      <div className="bg-white rounded-xl shadow p-4 flex flex-wrap gap-3">
        <input
          type="text"
          placeholder="Search by ID, category, area or weather"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 min-w-48 border border-slate-300 rounded-lg px-3 py-2 text-sm"
        />
        <select value={vehicle} onChange={(e) => setVehicle(e.target.value)} className={selectClass}>
          <option value="All">All vehicles</option>
          <option value="motorcycle">Motorcycle</option>
          <option value="scooter">Scooter</option>
          <option value="van">Van</option>
        </select>
        <select value={traffic} onChange={(e) => setTraffic(e.target.value)} className={selectClass}>
          <option value="All">All traffic</option>
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
          <option>Jam</option>
        </select>
      </div>

      {items.length === 0 ? (
        <div className="bg-white rounded-xl shadow p-8 text-center text-slate-500">
          No predictions yet. Open New Prediction to make your first one.
        </div>
      ) : shown.length === 0 ? (
        <div className="bg-white rounded-xl shadow p-8 text-center text-slate-500">
          No predictions match your search.
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow p-5">
          <p className="text-sm text-slate-500 mb-3">
            Showing {shown.length} of {items.length}
          </p>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-slate-500 border-b">
                <tr>
                  <th className="py-2 pr-4">ID</th>
                  <th className="py-2 pr-4">Vehicle</th>
                  <th className="py-2 pr-4">Traffic</th>
                  <th className="py-2 pr-4">Weather</th>
                  <th className="py-2 pr-4">Area</th>
                  <th className="py-2 pr-4">Category</th>
                  <th className="py-2 pr-4">Distance</th>
                  <th className="py-2 pr-4">Predicted</th>
                  <th className="py-2">Date</th>
                </tr>
              </thead>
              <tbody>
                {shown.map((item) => (
                  <tr key={item.id} className="border-b last:border-0">
                    <td className="py-2 pr-4">{item.id}</td>
                    <td className="py-2 pr-4">{item.vehicle}</td>
                    <td className="py-2 pr-4">{item.traffic}</td>
                    <td className="py-2 pr-4">{item.weather}</td>
                    <td className="py-2 pr-4">{item.area}</td>
                    <td className="py-2 pr-4">{item.category}</td>
                    <td className="py-2 pr-4">{item.distance_km} km</td>
                    <td className="py-2 pr-4">{item.predicted_minutes} min</td>
                    <td className="py-2 whitespace-nowrap">{new Date(item.created_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}