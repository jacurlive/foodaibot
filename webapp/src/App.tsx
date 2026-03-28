import { useEffect, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { useStore } from './store/useStore'
import { getMe } from './api/client'
import { useTelegram } from './hooks/useTelegram'
import { BottomNav } from './components/BottomNav'
import { Home } from './pages/Home'
import { Diary } from './pages/Diary'
import { Analyze } from './pages/Analyze'
import { Stats } from './pages/Stats'
import { Profile } from './pages/Profile'
import { Onboarding } from './pages/Onboarding'
import { PageLoader } from './components/Loader'
import './i18n'
import type { User } from './types'

type Tab = 'home' | 'diary' | 'analyze' | 'stats' | 'profile'

const pageVariants = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.3, ease: 'easeOut' } },
  exit: { opacity: 0, y: -8, transition: { duration: 0.2 } },
}

function NoTelegramScreen({ onLogin }: { onLogin: (id: number) => void }) {
  const [val, setVal] = useState('')
  const [err, setErr] = useState(false)

  const submit = () => {
    const id = parseInt(val.trim())
    if (!id || isNaN(id)) { setErr(true); return }
    localStorage.setItem('tg_user_id', String(id))
    onLogin(id)
  }

  return (
    <div className="h-full flex flex-col items-center justify-center gap-6 px-8"
      style={{ background: 'var(--bg-base)' }}>
      <div className="flex flex-col items-center gap-2">
        <span style={{ fontSize: 56 }}>🤖</span>
        <h1 className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>FoodAI</h1>
        <p className="text-sm text-center" style={{ color: 'var(--text-secondary)' }}>
          Введи Telegram ID для входа
        </p>
      </div>
      <div className="w-full flex flex-col gap-3">
        <input
          autoFocus
          type="number"
          placeholder="Telegram ID (напр. 819233688)"
          value={val}
          onChange={e => { setVal(e.target.value); setErr(false) }}
          onKeyDown={e => e.key === 'Enter' && submit()}
          className="w-full px-4 py-3 rounded-2xl text-center text-lg outline-none"
          style={{
            background: 'var(--bg-card)',
            border: `1.5px solid ${err ? 'var(--red)' : 'var(--border)'}`,
            color: 'var(--text-primary)',
          }}
        />
        {err && <p className="text-xs text-center" style={{ color: 'var(--red)' }}>Введи корректный ID</p>}
        <button
          onClick={submit}
          className="w-full py-3 rounded-2xl font-semibold text-base"
          style={{ background: 'var(--accent)', color: '#000' }}
        >
          Войти
        </button>
      </div>
    </div>
  )
}

function ErrorScreen({ message }: { message: string }) {
  return (
    <div className="h-full flex flex-col items-center justify-center gap-4 px-8"
      style={{ background: 'var(--bg-base)' }}>
      <span style={{ fontSize: 48 }}>⚠️</span>
      <p className="text-sm text-center" style={{ color: 'var(--text-secondary)' }}>{message}</p>
    </div>
  )
}

export default function App() {
  const { setUser, setTheme, theme } = useStore()
  const { getUserId } = useTelegram()
  const [tab, setTab] = useState<Tab>('home')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [user, setLocalUser] = useState<User | null>(null)
  const [noTelegram, setNoTelegram] = useState(false)

  useEffect(() => {
    setTheme(theme)
  }, [])

  useEffect(() => {
    const userId = getUserId()
    if (!userId) {
      setNoTelegram(true)
      setLoading(false)
      return
    }

    getMe()
      .then((u) => {
        setUser(u)
        setLocalUser(u)
        if (u.language) {
          import('i18next').then((i18next) => {
            i18next.default.changeLanguage(u.language)
          })
        }
      })
      .catch((err) => {
        const status = err?.response?.status
        if (status === 404) {
          setError('Сначала запустите бота командой /start')
        } else {
          setError('Не удалось загрузить данные. Попробуйте позже.')
        }
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center" style={{ background: 'var(--bg-base)' }}>
        <PageLoader />
      </div>
    )
  }

  if (noTelegram) return <NoTelegramScreen onLogin={() => window.location.reload()} />
  if (error) return <ErrorScreen message={error} />
  if (!user) return <ErrorScreen message="Ошибка загрузки" />

  if (!user.is_onboarded) {
    return (
      <div className="h-full" style={{ maxWidth: 480, margin: '0 auto' }}>
        <Onboarding
          user={user}
          onComplete={(updated) => {
            setLocalUser(updated)
            setUser(updated)
          }}
        />
      </div>
    )
  }

  const renderPage = () => {
    switch (tab) {
      case 'home':
        return <Home key="home" onNavigate={(t) => setTab(t as Tab)} />
      case 'diary':
        return <Diary key="diary" />
      case 'analyze':
        return <Analyze key="analyze" onNavigate={(t) => setTab(t as Tab)} />
      case 'stats':
        return <Stats key="stats" />
      case 'profile':
        return <Profile key="profile" />
    }
  }

  return (
    <div
      className="h-full flex flex-col"
      style={{ background: 'var(--bg-base)', maxWidth: 480, margin: '0 auto' }}
    >
      <div className="flex-1 overflow-hidden relative">
        <AnimatePresence mode="wait">
          <motion.div
            key={tab}
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
            className="absolute inset-0 flex flex-col"
          >
            {renderPage()}
          </motion.div>
        </AnimatePresence>
      </div>
      <BottomNav active={tab} onChange={(t) => setTab(t as Tab)} />
    </div>
  )
}
