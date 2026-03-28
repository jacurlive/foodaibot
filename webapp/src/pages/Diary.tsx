import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { getDiaryToday, getDiaryWeek, getDiaryHistory, deleteEntry } from '../api/client'
import { FoodCard } from '../components/FoodCard'
import { PageLoader } from '../components/Loader'
import type { DiaryToday, DiaryWeek, DiaryHistory, FoodEntry } from '../types'

type Tab = 'today' | 'yesterday' | 'week' | 'history'

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.35 } },
}

function TotalBar({ totals }: { totals: { calories: number; protein: number; fat: number; carbs: number } }) {
  const { t } = useTranslation()
  return (
    <div
      className="px-4 py-3 flex items-center justify-between"
      style={{
        background: 'var(--bg-surface)',
        borderTop: '1px solid var(--border-subtle)',
      }}
    >
      <span className="text-xs font-semibold" style={{ color: 'var(--text-secondary)' }}>
        {t('diary.total')}
      </span>
      <div className="flex items-center gap-3">
        <span className="text-sm font-bold" style={{ color: 'var(--accent)' }}>
          {Math.round(totals.calories)} {t('diary.calories')}
        </span>
        <span className="text-xs" style={{ color: 'var(--green)' }}>
          {t('diary.protein_short')} {Math.round(totals.protein)}г
        </span>
        <span className="text-xs" style={{ color: 'var(--orange)' }}>
          {t('diary.fat_short')} {Math.round(totals.fat)}г
        </span>
        <span className="text-xs" style={{ color: 'var(--blue)' }}>
          {t('diary.carbs_short')} {Math.round(totals.carbs)}г
        </span>
      </div>
    </div>
  )
}

export function Diary() {
  const { t } = useTranslation()
  const [activeTab, setActiveTab] = useState<Tab>('today')
  const [loading, setLoading] = useState(true)
  const [todayData, setTodayData] = useState<DiaryToday | null>(null)
  const [weekData, setWeekData] = useState<DiaryWeek | null>(null)
  const [historyData, setHistoryData] = useState<DiaryHistory | null>(null)
  const [historyPage, setHistoryPage] = useState(1)
  const [deletingId, setDeletingId] = useState<number | null>(null)

  useEffect(() => {
    setLoading(true)
    if (activeTab === 'today' || activeTab === 'yesterday') {
      getDiaryToday().then(setTodayData).finally(() => setLoading(false))
      if (activeTab === 'yesterday') {
        getDiaryWeek().then(setWeekData).finally(() => setLoading(false))
      }
    } else if (activeTab === 'week') {
      getDiaryWeek().then(setWeekData).finally(() => setLoading(false))
    } else {
      getDiaryHistory(historyPage).then(setHistoryData).finally(() => setLoading(false))
    }
  }, [activeTab, historyPage])

  const handleDelete = async (id: number) => {
    setDeletingId(id)
    try {
      await deleteEntry(id)
      // Refresh current view
      if (activeTab === 'today') {
        const data = await getDiaryToday()
        setTodayData(data)
      } else if (activeTab === 'week') {
        const data = await getDiaryWeek()
        setWeekData(data)
      } else if (activeTab === 'history') {
        const data = await getDiaryHistory(historyPage)
        setHistoryData(data)
      }
    } finally {
      setDeletingId(null)
    }
  }

  const tabs: { id: Tab; label: string }[] = [
    { id: 'today', label: t('diary.today') },
    { id: 'yesterday', label: t('diary.yesterday') },
    { id: 'week', label: t('diary.week') },
    { id: 'history', label: t('diary.history') },
  ]

  // Get yesterday's entries from week data
  const getYesterdayEntries = (): FoodEntry[] => {
    if (!weekData) return []
    const yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)
    const d = yesterday.toISOString().split('T')[0]
    return weekData.days.find((day) => day.date === d)?.entries || []
  }

  const getYesterdayTotals = () => {
    const entries = getYesterdayEntries()
    return {
      calories: entries.reduce((s, e) => s + e.calories, 0),
      protein: entries.reduce((s, e) => s + e.protein, 0),
      fat: entries.reduce((s, e) => s + e.fat, 0),
      carbs: entries.reduce((s, e) => s + e.carbs, 0),
    }
  }

  const renderEntries = (entries: FoodEntry[], showDelete = true) => {
    if (entries.length === 0) {
      return (
        <div className="text-center py-12">
          <p className="text-3xl mb-2">📭</p>
          <p className="font-medium" style={{ color: 'var(--text-secondary)' }}>
            {t('diary.no_entries')}
          </p>
          <p className="text-sm mt-1" style={{ color: 'var(--text-muted)' }}>
            {t('diary.empty_hint')}
          </p>
        </div>
      )
    }

    return (
      <AnimatePresence mode="popLayout">
        {entries.map((entry) => (
          <FoodCard
            key={entry.id}
            entry={entry}
            onDelete={showDelete ? handleDelete : undefined}
          />
        ))}
      </AnimatePresence>
    )
  }

  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      className="flex flex-col h-full"
    >
      {/* Header */}
      <div className="px-4 pt-4 pb-2" style={{ background: 'var(--bg-base)' }}>
        <h1 className="text-xl font-bold mb-3" style={{ color: 'var(--text-primary)' }}>
          {t('diary.title')}
        </h1>
        {/* Tab bar */}
        <div
          className="flex rounded-xl p-1 gap-1"
          style={{ background: 'var(--bg-card)' }}
        >
          {tabs.map((tab) => (
            <motion.button
              key={tab.id}
              whileTap={{ scale: 0.95 }}
              onClick={() => setActiveTab(tab.id)}
              className="flex-1 py-1.5 rounded-lg text-xs font-semibold transition-colors"
              style={{
                background: activeTab === tab.id ? 'var(--accent)' : 'transparent',
                color: activeTab === tab.id ? '#0B1410' : 'var(--text-muted)',
              }}
            >
              {tab.label}
            </motion.button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden flex flex-col">
        {loading ? (
          <div className="flex-1 flex items-center justify-center">
            <PageLoader />
          </div>
        ) : (
          <>
            <div className="scroll-area flex-1 px-4 py-3 flex flex-col gap-2">
              {activeTab === 'today' && renderEntries(todayData?.entries || [])}

              {activeTab === 'yesterday' && renderEntries(getYesterdayEntries())}

              {activeTab === 'week' && weekData && (
                <div className="flex flex-col gap-4">
                  {weekData.days
                    .filter((day) => day.entries.length > 0)
                    .reverse()
                    .map((day) => (
                      <div key={day.date}>
                        <div className="flex items-center justify-between mb-2">
                          <p className="text-sm font-semibold" style={{ color: 'var(--text-secondary)' }}>
                            {new Date(day.date + 'T00:00:00').toLocaleDateString('ru', {
                              weekday: 'short',
                              day: 'numeric',
                              month: 'short',
                            })}
                          </p>
                          <span className="text-xs font-bold" style={{ color: 'var(--accent)' }}>
                            {Math.round(day.totals.calories)} ккал
                          </span>
                        </div>
                        <div className="flex flex-col gap-2">
                          {day.entries.map((entry) => (
                            <FoodCard key={entry.id} entry={entry} onDelete={handleDelete} />
                          ))}
                        </div>
                      </div>
                    ))}
                  {weekData.days.every((d) => d.entries.length === 0) && (
                    <div className="text-center py-12">
                      <p className="text-3xl mb-2">📭</p>
                      <p style={{ color: 'var(--text-secondary)' }}>{t('diary.no_entries')}</p>
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'history' && historyData && (
                <div className="flex flex-col gap-2">
                  {renderEntries(historyData.entries, false)}
                  {historyData.pages > 1 && (
                    <div className="flex items-center justify-center gap-3 py-2">
                      <motion.button
                        whileTap={{ scale: 0.9 }}
                        onClick={() => setHistoryPage((p) => Math.max(1, p - 1))}
                        disabled={historyPage === 1}
                        className="px-4 py-2 rounded-xl text-sm font-medium disabled:opacity-40"
                        style={{
                          background: 'var(--bg-card)',
                          border: '1px solid var(--border)',
                          color: 'var(--text-secondary)',
                        }}
                      >
                        ←
                      </motion.button>
                      <span className="text-sm" style={{ color: 'var(--text-muted)' }}>
                        {t('diary.page')} {historyPage} / {historyData.pages}
                      </span>
                      <motion.button
                        whileTap={{ scale: 0.9 }}
                        onClick={() => setHistoryPage((p) => Math.min(historyData.pages, p + 1))}
                        disabled={historyPage === historyData.pages}
                        className="px-4 py-2 rounded-xl text-sm font-medium disabled:opacity-40"
                        style={{
                          background: 'var(--bg-card)',
                          border: '1px solid var(--border)',
                          color: 'var(--text-secondary)',
                        }}
                      >
                        →
                      </motion.button>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Sticky totals */}
            {activeTab === 'today' && todayData && todayData.entries.length > 0 && (
              <TotalBar totals={todayData.totals} />
            )}
            {activeTab === 'yesterday' && getYesterdayEntries().length > 0 && (
              <TotalBar totals={getYesterdayTotals()} />
            )}
          </>
        )}
      </div>
    </motion.div>
  )
}
