import { useEffect, useState } from 'react'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import api from '../api'
import StatCard from '../components/StatCard'

interface Overview {
  total_predictions: number
  average_minutes: number
  shortest_minutes: number
  longest_minutes: number
}

interface Group {
  name: string
  count: number
  average_minutes: number
}

interface Record {
  id: number
  vehicle: string
  traffic: string
  distance_km: number
  predicted_minutes: number
  created_at: string
}

const trafficOrder = ['Low', 'Medium', 'High', 'Jam']

function Chart({ title, data }: { title: string; data: Group[] }) {
  return (
    <div className="bg-white rounded-xl shadow p-5">
      <h3 className="font-semibold text-slate-700 mb-4">{title}</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis unit=" min" width={70} />
            <Tooltip />
            <Bar dataKey="average_minutes" name="Average minutes" fill="#2563eb" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [overview, setOverview] = useState<Overview | null>(null)
  const [byVehicle, setByVehicle] = useState<Group[]>([])
  const [byTraffic, setByTraffic] = useState<Group[]>([])
  const [recent, setRecent] = useState<Record[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      api.get('/api/v1/analytics/overview'),
      api.get('/api/v1/analytics/delivery-performance'),
      api.get('/api/v1/predictions'),
    ])
      .then(([overviewRes, performanceRes, recentRes]) => {
        setOverview(overviewRes.data)
        setByVehicle(performanceRes.data.by_vehicle)
        const traffic: Group[] = performanceRes.data.by_traffic
        setByTraffic([...traffic].sort((a, b) => trafficOrder.indexOf(a.name) - trafficOrder.indexOf(b.name)))
        setRecent(recentRes.data.slice(0, 5))
      })
      .catch(() => setError('Could not load the dashboard. Please try again.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="text-slate-500">Loading...</p>
  if (error) return <p className="bg-red-50 text-red-600 rounded-lg p-3">{error}</p>

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold text-slate-800">Dashboard</h2>

      {overview && overview.total_predictions === 0 ? (
        <div className="bg-white rounded-xl shadow p-8 text-center text-slate-500">
          No predictions yet. Open New Prediction to make your first one.
        </div>
      ) : (
        <>
          <div className="grid gap-4 grid-cols-2 lg:grid-cols-4">
            <StatCard label="Total predictions" value={String(overview?.total_predictions ?? 0)} />
            <StatCard label="Average time" value={`${overview?.average_minutes ?? 0} min`} />
            <StatCard label="Shortest" value={`${overview?.shortest_minutes ?? 0} min`} />
            <StatCard label="Longest" value={`${overview?.longest_minutes ?? 0} min`} />
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <Chart title="Average predicted time by vehicle" data={byVehicle} />
            <Chart title="Average predicted time by traffic" data={byTraffic} />
          </div>

          <div className="bg-white rounded-xl shadow p-5">
            <h3 className="font-semibold text-slate-700 mb-4">Recent predictions</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-slate-500 border-b">
                  <tr>
                    <th className="py-2 pr-4">ID</th>
                    <th className="py-2 pr-4">Vehicle</th>
                    <th className="py-2 pr-4">Traffic</th>
                    <th className="py-2 pr-4">Distance</th>
                    <th className="py-2 pr-4">Predicted</th>
                    <th className="py-2">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {recent.map((item) => (
                    <tr key={item.id} className="border-b last:border-0">
                      <td className="py-2 pr-4">{item.id}</td>
                      <td className="py-2 pr-4">{item.vehicle}</td>
                      <td className="py-2 pr-4">{item.traffic}</td>
                      <td className="py-2 pr-4">{item.distance_km} km</td>
                      <td className="py-2 pr-4">{item.predicted_minutes} min</td>
                      <td className="py-2">{new Date(item.created_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  )
}