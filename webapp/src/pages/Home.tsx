import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { Sun, Moon, ChevronRight } from 'lucide-react'
import { useStore } from '../store/useStore'
import { getDiaryToday } from '../api/client'
import { CalorieRing } from '../components/CalorieRing'
import { MacroBar } from '../components/MacroBar'
import { FoodCard } from '../components/FoodCard'
import { PageLoader } from '../components/Loader'
import type { DiaryToday } from '../types'

interface HomeProps {
  onNavigate: (tab: string) => void
}

function getGreeting(t: (key: string) => string): string {
  const h = new Date().getHours()
  if (h < 12) return t('home.greeting_morning')
  if (h < 18) return t('home.greeting_afternoon')
  return t('home.greeting_evening')
}

function formatDateFull(): string {
  return new Date().toLocaleDateString('ru', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  })
}

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.35, ease: 'easeOut' } },
}

const stagger = {
  animate: {
    transition: { staggerChildren: 0.05 },
  },
}

const itemVariants = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.3 } },
}

export function Home({ onNavigate }: HomeProps) {
  const { t } = useTranslation()
  const { user, theme, toggleTheme } = useStore()
  const [diary, setDiary] = useState<DiaryToday | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getDiaryToday()
      .then(setDiary)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <PageLoader />

  const name = user?.name || user?.first_name || ''
  const goal = user?.daily_calories || 2000
  const totals = diary?.totals || { calories: 0, protein: 0, fat: 0, carbs: 0 }
  const remaining = diary?.remaining_calories || goal
  const recentEntries = (diary?.entries || []).slice(-3).reverse()

  // Estimated macro targets (rough)
  const proteinGoal = Math.round((goal * 0.25) / 4)
  const fatGoal = Math.round((goal * 0.30) / 9)
  const carbsGoal = Math.round((goal * 0.45) / 4)

  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      className="flex flex-col h-full"
    >
      <div className="scroll-area flex-1 px-4 pb-4">
        {/* Header */}
        <div className="flex items-start justify-between pt-4 pb-2">
          <div>
            <h1 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>
              {getGreeting(t)}{name ? `, ${name}` : ''}
            </h1>
            <p className="text-sm capitalize mt-0.5" style={{ color: 'var(--text-secondary)' }}>
              {formatDateFull()}
            </p>
          </div>
          <motion.button
            whileTap={{ scale: 0.85 }}
            onClick={toggleTheme}
            className="w-9 h-9 rounded-xl flex items-center justify-center mt-1"
            style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)' }}
          >
            {theme === 'dark' ? (
              <Sun size={17} style={{ color: 'var(--accent)' }} />
            ) : (
              <Moon size={17} style={{ color: 'var(--text-secondary)' }} />
            )}
          </motion.button>
        </div>

        <motion.div variants={stagger} initial="initial" animate="animate" className="flex flex-col gap-4">
          {/* Calorie Ring */}
          <motion.div
            variants={itemVariants}
            className="flex flex-col items-center py-4 rounded-2xl"
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <CalorieRing consumed={totals.calories} goal={goal} size={190} />
            <div className="flex gap-6 mt-3">
              <div className="text-center">
                <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{t('home.calories_consumed')}</p>
                <p className="font-bold text-sm mt-0.5" style={{ color: 'var(--accent)' }}>
                  {Math.round(totals.calories)}
                </p>
              </div>
              <div className="w-px" style={{ background: 'var(--border)' }} />
              <div className="text-center">
                <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{t('home.calories_remaining')}</p>
                <p className="font-bold text-sm mt-0.5" style={{ color: 'var(--text-primary)' }}>
                  {Math.round(remaining)}
                </p>
              </div>
              <div className="w-px" style={{ background: 'var(--border)' }} />
              <div className="text-center">
                <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{t('home.goal')}</p>
                <p className="font-bold text-sm mt-0.5" style={{ color: 'var(--text-secondary)' }}>
                  {Math.round(goal)}
                </p>
              </div>
            </div>
          </motion.div>

          {/* Macros */}
          <motion.div
            variants={itemVariants}
            className="rounded-2xl p-4"
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div className="grid grid-cols-3 gap-3 mb-4">
              {[
                { label: t('home.macro_protein'), value: totals.protein, color: 'var(--green)', emoji: '🥩' },
                { label: t('home.macro_fat'), value: totals.fat, color: 'var(--orange)', emoji: '🧈' },
                { label: t('home.macro_carbs'), value: totals.carbs, color: 'var(--blue)', emoji: '🍞' },
              ].map((macro) => (
                <div
                  key={macro.label}
                  className="flex flex-col items-center gap-1 rounded-xl p-2"
                  style={{ background: 'var(--bg-elevated)' }}
                >
                  <span className="text-base">{macro.emoji}</span>
                  <span className="text-base font-bold" style={{ color: macro.color }}>
                    {Math.round(macro.value)}г
                  </span>
                  <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
                    {macro.label}
                  </span>
                </div>
              ))}
            </div>
            <div className="flex flex-col gap-3">
              <MacroBar
                label={t('home.macro_protein')}
                value={totals.protein}
                max={proteinGoal}
                color="var(--green)"
              />
              <MacroBar
                label={t('home.macro_fat')}
                value={totals.fat}
                max={fatGoal}
                color="var(--orange)"
              />
              <MacroBar
                label={t('home.macro_carbs')}
                value={totals.carbs}
                max={carbsGoal}
                color="var(--blue)"
              />
            </div>
          </motion.div>

          {/* Recent meals */}
          <motion.div variants={itemVariants}>
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-semibold text-sm" style={{ color: 'var(--text-primary)' }}>
                {t('home.recent_meals')}
              </h2>
              {recentEntries.length > 0 && (
                <motion.button
                  whileTap={{ scale: 0.92 }}
                  onClick={() => onNavigate('diary')}
                  className="flex items-center gap-1 text-xs font-medium"
                  style={{ color: 'var(--accent)' }}
                >
                  {t('home.view_all')}
                  <ChevronRight size={13} />
                </motion.button>
              )}
            </div>

            <AnimatePresence mode="popLayout">
              {recentEntries.length === 0 ? (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-8 rounded-2xl"
                  style={{
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border-subtle)',
                  }}
                >
                  <p className="text-3xl mb-2">🍽</p>
                  <p className="font-medium text-sm" style={{ color: 'var(--text-secondary)' }}>
                    {t('home.no_entries_today')}
                  </p>
                  <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>
                    {t('home.add_first')}
                  </p>
                </motion.div>
              ) : (
                <div className="flex flex-col gap-2">
                  {recentEntries.map((entry) => (
                    <FoodCard key={entry.id} entry={entry} compact />
                  ))}
                </div>
              )}
            </AnimatePresence>
          </motion.div>

          {/* Remaining strip */}
          {remaining > 0 && totals.calories > 0 && (
            <motion.div
              variants={itemVariants}
              className="rounded-2xl p-3 flex items-center gap-3"
              style={{
                background: 'linear-gradient(135deg, rgba(245,158,11,0.12), rgba(249,115,22,0.08))',
                border: '1px solid rgba(245,158,11,0.2)',
              }}
            >
              <span className="text-xl">🔥</span>
              <p className="text-sm font-semibold" style={{ color: 'var(--accent)' }}>
                {t('home.remaining')} {Math.round(remaining)} {t('home.kcal')}
              </p>
            </motion.div>
          )}
        </motion.div>
      </div>
    </motion.div>
  )
}
