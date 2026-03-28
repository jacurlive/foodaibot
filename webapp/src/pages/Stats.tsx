import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useTranslation } from 'react-i18next'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'
import { Flame, TrendingUp, UtensilsCrossed } from 'lucide-react'
import { getStatsOverview } from '../api/client'
import { useStore } from '../store/useStore'
import { WeekChart } from '../components/WeekChart'
import { StatCard } from '../components/StatCard'
import { MacroBar } from '../components/MacroBar'
import { PageLoader } from '../components/Loader'
import type { StatsOverview } from '../types'

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.35 } },
}

const sectionVariants = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
}

function MacroPieChart({ data }: { data: { protein: number; fat: number; carbs: number } }) {
  const { t } = useTranslation()
  const total = data.protein + data.fat + data.carbs
  const chartData = [
    { name: t('stats.protein'), value: data.protein, color: 'var(--green)' },
    { name: t('stats.fat'), value: data.fat, color: 'var(--orange)' },
    { name: t('stats.carbs'), value: data.carbs, color: 'var(--blue)' },
  ]

  return (
    <div className="relative">
      <ResponsiveContainer width="100%" height={160}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={50}
            outerRadius={70}
            paddingAngle={3}
            dataKey="value"
            animationBegin={0}
            animationDuration={800}
          >
            {chartData.map((entry, idx) => (
              <Cell key={idx} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value: number) => [`${Math.round(value)}г`, '']}
            contentStyle={{
              background: 'var(--bg-elevated)',
              border: '1px solid var(--border)',
              borderRadius: '12px',
              color: 'var(--text-primary)',
              fontSize: 12,
            }}
          />
        </PieChart>
      </ResponsiveContainer>
      {/* Center label */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className="text-center">
          <p className="text-sm font-bold" style={{ color: 'var(--text-primary)' }}>
            {Math.round(total)}г
          </p>
          <p style={{ fontSize: 10, color: 'var(--text-muted)' }}>макро</p>
        </div>
      </div>
    </div>
  )
}

function MonthlyHeatmap({ data }: { data: Array<{ date: string; calories: number }> }) {
  if (data.length === 0) return null

  const maxCalories = Math.max(...data.map((d) => d.calories), 1)

  function getColor(calories: number): string {
    if (calories === 0) return 'var(--border)'
    const ratio = calories / maxCalories
    if (ratio < 0.33) return 'rgba(245,158,11,0.25)'
    if (ratio < 0.66) return 'rgba(245,158,11,0.6)'
    return 'var(--accent)'
  }

  return (
    <div
      className="grid gap-1"
      style={{ gridTemplateColumns: 'repeat(10, 1fr)' }}
    >
      {data.map((d) => (
        <motion.div
          key={d.date}
          initial={{ opacity: 0, scale: 0.7 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.2 }}
          title={`${d.date}: ${Math.round(d.calories)} ккал`}
          className="rounded-md aspect-square"
          style={{ background: getColor(d.calories) }}
        />
      ))}
    </div>
  )
}

export function Stats() {
  const { t } = useTranslation()
  const { user } = useStore()
  const [stats, setStats] = useState<StatsOverview | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getStatsOverview()
      .then(setStats)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <PageLoader />

  if (!stats || stats.total_entries === 0) {
    return (
      <motion.div
        variants={pageVariants}
        initial="initial"
        animate="animate"
        className="flex flex-col h-full items-center justify-center px-8 text-center gap-4"
      >
        <p className="text-5xl">📊</p>
        <p className="text-lg font-bold" style={{ color: 'var(--text-primary)' }}>
          {t('stats.no_data')}
        </p>
        <p className="text-sm" style={{ color: 'var(--text-muted)' }}>
          {t('stats.start_tracking')}
        </p>
      </motion.div>
    )
  }

  const goal = user?.daily_calories || 2000
  const macroMaxWeek = {
    protein: Math.max(1, stats.macro_avg_week.protein * 1.5),
    fat: Math.max(1, stats.macro_avg_week.fat * 1.5),
    carbs: Math.max(1, stats.macro_avg_week.carbs * 1.5),
  }

  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      className="flex flex-col h-full"
    >
      <div className="scroll-area flex-1 px-4 pb-6">
        <div className="pt-4 pb-2">
          <h1 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>
            {t('stats.title')}
          </h1>
        </div>

        <div className="flex flex-col gap-4">
          {/* Stat cards row */}
          <motion.div
            variants={sectionVariants}
            initial="initial"
            animate="animate"
            transition={{ delay: 0.05 }}
            className="flex gap-3"
          >
            <StatCard
              index={0}
              icon={<Flame size={16} />}
              label={t('stats.streak')}
              value={stats.streak_days}
              unit={t('stats.streak_unit')}
              color="var(--orange)"
            />
            <StatCard
              index={1}
              icon={<TrendingUp size={16} />}
              label={t('stats.avg_day')}
              value={Math.round(stats.avg_calories_per_day)}
              unit={t('stats.kcal')}
              color="var(--accent)"
            />
            <StatCard
              index={2}
              icon={<UtensilsCrossed size={16} />}
              label={t('stats.total_meals')}
              value={stats.total_entries}
              color="var(--cyan)"
            />
          </motion.div>

          {/* Weekly chart */}
          <motion.div
            variants={sectionVariants}
            initial="initial"
            animate="animate"
            transition={{ delay: 0.1 }}
            className="rounded-2xl p-4"
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                {t('stats.weekly_chart')}
              </h2>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-1 rounded-full" style={{ background: 'var(--accent)' }} />
                <span className="text-xs" style={{ color: 'var(--text-muted)' }}>ккал</span>
                <div
                  className="w-3 h-px rounded"
                  style={{ borderTop: '2px dashed var(--red)', marginLeft: 6 }}
                />
                <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{t('stats.goal_line')}</span>
              </div>
            </div>
            <WeekChart data={stats.weekly_calories} goal={goal} />
          </motion.div>

          {/* Macro breakdown */}
          <motion.div
            variants={sectionVariants}
            initial="initial"
            animate="animate"
            transition={{ delay: 0.15 }}
            className="rounded-2xl p-4"
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <h2 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>
              {t('stats.macro_breakdown')}
            </h2>
            <div className="flex gap-4">
              <div className="flex-1">
                <MacroPieChart data={stats.macro_totals_week} />
              </div>
              <div className="flex-1 flex flex-col justify-center gap-3">
                <MacroBar
                  label={t('stats.protein')}
                  value={stats.macro_avg_week.protein}
                  max={macroMaxWeek.protein}
                  color="var(--green)"
                />
                <MacroBar
                  label={t('stats.fat')}
                  value={stats.macro_avg_week.fat}
                  max={macroMaxWeek.fat}
                  color="var(--orange)"
                />
                <MacroBar
                  label={t('stats.carbs')}
                  value={stats.macro_avg_week.carbs}
                  max={macroMaxWeek.carbs}
                  color="var(--blue)"
                />
              </div>
            </div>
          </motion.div>

          {/* Best day */}
          {stats.best_day && (
            <motion.div
              variants={sectionVariants}
              initial="initial"
              animate="animate"
              transition={{ delay: 0.2 }}
              className="rounded-2xl p-4 flex items-center gap-4"
              style={{
                background: 'linear-gradient(135deg, rgba(245,158,11,0.12), rgba(249,115,22,0.06))',
                border: '1px solid rgba(245,158,11,0.2)',
              }}
            >
              <span className="text-3xl">🏆</span>
              <div>
                <p className="text-xs font-medium" style={{ color: 'var(--text-muted)' }}>
                  {t('stats.best_day')}
                </p>
                <p className="font-bold text-base mt-0.5" style={{ color: 'var(--accent)' }}>
                  {new Date(stats.best_day + 'T00:00:00').toLocaleDateString('ru', {
                    weekday: 'long',
                    day: 'numeric',
                    month: 'long',
                  })}
                </p>
              </div>
            </motion.div>
          )}

          {/* Monthly heatmap */}
          <motion.div
            variants={sectionVariants}
            initial="initial"
            animate="animate"
            transition={{ delay: 0.25 }}
            className="rounded-2xl p-4"
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <h2 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>
              {t('stats.monthly_activity')}
            </h2>
            <MonthlyHeatmap data={stats.monthly_calories} />
            <div className="flex items-center justify-end gap-3 mt-3">
              {[
                { color: 'var(--border)', label: '0' },
                { color: 'rgba(245,158,11,0.25)', label: '< 50%' },
                { color: 'rgba(245,158,11,0.6)', label: '50–80%' },
                { color: 'var(--accent)', label: '> 80%' },
              ].map((item) => (
                <div key={item.label} className="flex items-center gap-1">
                  <div
                    className="w-3 h-3 rounded-sm"
                    style={{ background: item.color }}
                  />
                  <span className="text-xs" style={{ color: 'var(--text-muted)' }}>{item.label}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
}
