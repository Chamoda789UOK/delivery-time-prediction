import { useEffect, useState } from 'react'
import api from '../api'
import StatCard from '../components/StatCard'

interface Info {
  model_version: string
  training_date: string
  dataset: string
  target: string
  features: string[]
  architecture: string
  metrics: { mae: number; rmse: number; r2: number }
}

const limitations = [
  'The model was trained on food and parcel delivery data from India, not truck logistics.',
  'It does not use real-time traffic or live weather. Traffic and weather are chosen by the user.',
  'The delivery agent age and rating strongly affect the result in this dataset.',
  'Traffic has a smaller effect than expected in real life.',
  'A Random Forest model scored about the same as this neural network on the test data.',
  'The result is an estimate. It is not a guaranteed arrival time.',
]

export default function ModelInfo() {
  const [info, setInfo] = useState<Info | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/api/v1/model/info')
      .then((res) => setInfo(res.data))
      .catch(() => setError('Could not load the model information. Please try again.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="text-slate-500">Loading...</p>
  if (error || !info) return <p className="bg-red-50 text-red-600 rounded-lg p-3">{error}</p>

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold text-slate-800">Model Information</h2>

      <div className="grid gap-4 grid-cols-2 lg:grid-cols-4">
        <StatCard label="Version" value={info.model_version} />
        <StatCard label="MAE (test)" value={`${info.metrics.mae} min`} />
        <StatCard label="RMSE (test)" value={`${info.metrics.rmse} min`} />
        <StatCard label="R² (test)" value={String(info.metrics.r2)} />
      </div>

      <div className="bg-white rounded-xl shadow p-5 space-y-3 text-sm">
        <h3 className="font-semibold text-slate-700">Training details</h3>
        <p><span className="text-slate-500">Trained on:</span> {info.training_date}</p>
        <p><span className="text-slate-500">Dataset:</span> {info.dataset}</p>
        <p><span className="text-slate-500">Target:</span> {info.target}</p>
        <p><span className="text-slate-500">Architecture:</span> {info.architecture}</p>
      </div>

      <div className="bg-white rounded-xl shadow p-5">
        <h3 className="font-semibold text-slate-700 mb-3">Input features</h3>
        <div className="flex flex-wrap gap-2">
          {info.features.map((feature) => (
            <span key={feature} className="bg-blue-50 text-blue-700 rounded-full px-3 py-1 text-sm">
              {feature}
            </span>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-xl shadow p-5">
        <h3 className="font-semibold text-slate-700 mb-3">Limitations</h3>
        <ul className="list-disc pl-5 space-y-1 text-sm text-slate-700">
          {limitations.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}