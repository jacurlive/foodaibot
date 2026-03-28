import { motion } from 'framer-motion'
import { Trash2 } from 'lucide-react'
import type { FoodEntry } from '../types'

interface FoodCardProps {
  entry: FoodEntry
  onDelete?: (id: number) => void
  compact?: boolean
}

function formatTime(dateStr: string) {
  const d = new Date(dateStr)
  return d.toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' })
}

export function FoodCard({ entry, onDelete, compact = false }: FoodCardProps) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -40, transition: { duration: 0.2 } }}
      className="relative rounded-xl p-3 flex items-center gap-3"
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-subtle)',
      }}
    >
      {/* Dish icon */}
      <div
        className="w-10 h-10 rounded-xl flex items-center justify-center text-lg flex-shrink-0"
        style={{ background: 'var(--bg-elevated)' }}
      >
        🍽
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <p
          className="font-semibold text-sm truncate"
          style={{ color: 'var(--text-primary)' }}
        >
          {entry.dish_name}
        </p>
        <div className="flex items-center gap-2 mt-0.5 flex-wrap">
          <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
            {formatTime(entry.eaten_at)}
          </span>
          <span className="text-xs font-bold" style={{ color: 'var(--accent)' }}>
            {Math.round(entry.calories)} ккал
          </span>
          {!compact && (
            <>
              <span
                className="text-xs px-1.5 py-0.5 rounded-full"
                style={{ background: 'rgba(52,211,153,0.12)', color: 'var(--green)' }}
              >
                Б {Math.round(entry.protein)}г
              </span>
              <span
                className="text-xs px-1.5 py-0.5 rounded-full"
                style={{ background: 'rgba(251,146,60,0.12)', color: 'var(--orange)' }}
              >
                Ж {Math.round(entry.fat)}г
              </span>
              <span
                className="text-xs px-1.5 py-0.5 rounded-full"
                style={{ background: 'rgba(96,165,250,0.12)', color: 'var(--blue)' }}
              >
                У {Math.round(entry.carbs)}г
              </span>
            </>
          )}
        </div>
      </div>

      {/* Delete button */}
      {onDelete && (
        <motion.button
          whileTap={{ scale: 0.85 }}
          onClick={() => onDelete(entry.id)}
          className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
          style={{
            background: 'rgba(248,113,113,0.1)',
            color: 'var(--red)',
          }}
        >
          <Trash2 size={15} />
        </motion.button>
      )}
    </motion.div>
  )
}
