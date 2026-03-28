import { motion } from 'framer-motion'

interface LoaderProps {
  size?: 'sm' | 'md' | 'lg'
  text?: string
}

export function Loader({ size = 'md', text }: LoaderProps) {
  const sizes = { sm: 24, md: 40, lg: 56 }
  const s = sizes[size]
  const stroke = size === 'sm' ? 2 : 3

  return (
    <div className="flex flex-col items-center justify-center gap-3">
      <motion.svg
        width={s}
        height={s}
        viewBox="0 0 40 40"
        fill="none"
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      >
        <circle cx="20" cy="20" r="16" stroke="var(--border)" strokeWidth={stroke} />
        <path
          d="M20 4 A16 16 0 0 1 36 20"
          stroke="var(--accent)"
          strokeWidth={stroke}
          strokeLinecap="round"
        />
      </motion.svg>
      {text && (
        <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{text}</p>
      )}
    </div>
  )
}

export function PageLoader() {
  return (
    <div className="flex items-center justify-center h-full">
      <Loader size="lg" />
    </div>
  )
}
