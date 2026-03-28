import { motion } from 'framer-motion'

interface MacroBarProps {
  label: string
  value: number
  max?: number
  color: string
  unit?: string
}

export function MacroBar({ label, value, max = 100, color, unit = 'г' }: MacroBarProps) {
  const percent = Math.min(1, max > 0 ? value / max : 0)

  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>
          {label}
        </span>
        <span className="text-xs font-bold" style={{ color }}>
          {Math.round(value)}{unit}
        </span>
      </div>
      <div
        className="h-1.5 rounded-full overflow-hidden"
        style={{ background: 'var(--border)' }}
      >
        <motion.div
          className="h-full rounded-full"
          style={{ background: color }}
          initial={{ width: 0 }}
          animate={{ width: `${percent * 100}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
        />
      </div>
    </div>
  )
}
