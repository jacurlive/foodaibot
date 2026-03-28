import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface StatCardProps {
  icon: ReactNode
  label: string
  value: string | number
  unit?: string
  color?: string
  index?: number
}

export function StatCard({ icon, label, value, unit, color = 'var(--accent)', index = 0 }: StatCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08, duration: 0.35 }}
      className="flex flex-col gap-1.5 rounded-2xl p-3 flex-1"
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-subtle)',
      }}
    >
      <div
        className="w-8 h-8 rounded-xl flex items-center justify-center text-base"
        style={{ background: `${color}20` }}
      >
        <span style={{ color }}>{icon}</span>
      </div>
      <div>
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>
            {value}
          </span>
          {unit && (
            <span className="text-xs font-medium" style={{ color: 'var(--text-muted)' }}>
              {unit}
            </span>
          )}
        </div>
        <p className="text-xs mt-0.5" style={{ color: 'var(--text-secondary)' }}>
          {label}
        </p>
      </div>
    </motion.div>
  )
}
