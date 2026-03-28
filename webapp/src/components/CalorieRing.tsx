import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'

interface CalorieRingProps {
  consumed: number
  goal: number
  size?: number
}

export function CalorieRing({ consumed, goal, size = 200 }: CalorieRingProps) {
  const radius = (size - 24) / 2
  const circumference = 2 * Math.PI * radius
  const percent = Math.min(1, goal > 0 ? consumed / goal : 0)
  const isOver = consumed > goal

  const [animatedPercent, setAnimatedPercent] = useState(0)

  useEffect(() => {
    const timeout = setTimeout(() => setAnimatedPercent(percent), 100)
    return () => clearTimeout(timeout)
  }, [percent])

  const offset = circumference * (1 - animatedPercent)
  const strokeColor = isOver ? 'var(--red)' : 'var(--accent)'

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--border)"
          strokeWidth={10}
        />
        {/* Glow */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={strokeColor}
          strokeWidth={10}
          strokeOpacity={0.15}
        />
        {/* Progress arc */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={strokeColor}
          strokeWidth={10}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: 'easeOut' }}
        />
      </svg>

      {/* Center text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span
          className="text-3xl font-bold"
          style={{ color: isOver ? 'var(--red)' : 'var(--text-primary)' }}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.4 }}
        >
          {Math.round(consumed)}
        </motion.span>
        <span className="text-xs mt-0.5" style={{ color: 'var(--text-muted)' }}>
          из {Math.round(goal)} ккал
        </span>
        <motion.span
          className="text-sm font-semibold mt-1"
          style={{ color: isOver ? 'var(--red)' : 'var(--accent)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          {Math.round(percent * 100)}%
        </motion.span>
      </div>
    </div>
  )
}
