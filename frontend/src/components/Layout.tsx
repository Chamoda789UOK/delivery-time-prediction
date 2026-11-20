import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../AuthContext'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/predict', label: 'New Prediction' },
  { to: '/history', label: 'History' },
  { to: '/model', label: 'Model Info' },
]

export default function Layout() {
  const { logout } = useAuth()

  return (
    <div className="min-h-screen bg-slate-100 md:flex">
      <aside className="bg-slate-900 text-white md:w-60 md:min-h-screen p-4 flex md:flex-col gap-2 items-center md:items-stretch">
        <h1 className="font-bold text-lg md:mb-6 mr-4 md:mr-0">Delivery AI</h1>
        <nav className="flex md:flex-col gap-2 flex-1">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end
              className={({ isActive }) =>
                `rounded-lg px-3 py-2 text-sm ${isActive ? 'bg-blue-600' : 'hover:bg-slate-800'}`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
        <button onClick={logout} className="text-sm text-slate-300 hover:text-white rounded-lg px-3 py-2 text-left">
          Log out
        </button>
      </aside>
      <main className="flex-1 p-4 md:p-8">
        <Outlet />
      </main>
    </div>
  )
}