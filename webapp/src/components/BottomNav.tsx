import { motion } from 'framer-motion'
import { Home, BookOpen, Camera, BarChart2, User } from 'lucide-react'
import { useTranslation } from 'react-i18next'

interface BottomNavProps {
  active: string
  onChange: (tab: string) => void
}

const tabs = [
  { id: 'home', icon: Home, labelKey: 'nav.home' },
  { id: 'diary', icon: BookOpen, labelKey: 'nav.diary' },
  { id: 'analyze', icon: Camera, labelKey: 'nav.analyze', center: true },
  { id: 'stats', icon: BarChart2, labelKey: 'nav.stats' },
  { id: 'profile', icon: User, labelKey: 'nav.profile' },
]

export function BottomNav({ active, onChange }: BottomNavProps) {
  const { t } = useTranslation()

  return (
    <nav
      className="flex items-center justify-around px-2 pb-safe"
      style={{
        background: 'var(--bg-surface)',
        borderTop: '1px solid var(--border-subtle)',
        minHeight: 60,
        paddingBottom: 'max(env(safe-area-inset-bottom, 0px), 8px)',
      }}
    >
      {tabs.map((tab) => {
        const Icon = tab.icon
        const isActive = active === tab.id

        if (tab.center) {
          return (
            <motion.button
              key={tab.id}
              whileTap={{ scale: 0.88 }}
              onClick={() => onChange(tab.id)}
              className="relative -mt-5 w-14 h-14 rounded-full flex items-center justify-center shadow-lg"
              style={{
                background: isActive
                  ? 'var(--accent)'
                  : 'linear-gradient(135deg, var(--accent), #F97316)',
                boxShadow: '0 4px 20px rgba(245,158,11,0.4)',
              }}
            >
              <Icon size={22} color="#0B1410" strokeWidth={2.5} />
            </motion.button>
          )
        }

        return (
          <motion.button
            key={tab.id}
            whileTap={{ scale: 0.9 }}
            onClick={() => onChange(tab.id)}
            className="flex flex-col items-center gap-0.5 py-1 px-3 rounded-xl transition-colors"
            style={{
              minWidth: 52,
            }}
          >
            <motion.div
              animate={{ scale: isActive ? 1.1 : 1 }}
              transition={{ type: 'spring', stiffness: 400, damping: 25 }}
            >
              <Icon
                size={20}
                style={{
                  color: isActive ? 'var(--accent)' : 'var(--text-muted)',
                  strokeWidth: isActive ? 2.5 : 1.8,
                }}
              />
            </motion.div>
            <span
              className="text-xs"
              style={{
                color: isActive ? 'var(--accent)' : 'var(--text-muted)',
                fontWeight: isActive ? 600 : 400,
                fontSize: '10px',
              }}
            >
              {t(tab.labelKey)}
            </span>
          </motion.button>
        )
      })}
    </nav>
  )
}
