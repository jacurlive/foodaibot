import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
  Cell,
} from 'recharts'
import type { CalorieDay } from '../types'

interface WeekChartProps {
  data: CalorieDay[]
  goal: number
}

function formatDate(dateStr: string) {
  const d = new Date(dateStr + 'T00:00:00')
  return d.toLocaleDateString('ru', { weekday: 'short' }).slice(0, 2)
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div
        className="rounded-xl px-3 py-2 text-sm"
        style={{
          background: 'var(--bg-elevated)',
          border: '1px solid var(--border)',
          color: 'var(--text-primary)',
        }}
      >
        <p className="font-bold" style={{ color: 'var(--accent)' }}>
          {Math.round(payload[0].value)} ккал
        </p>
        <p style={{ color: 'var(--text-muted)', fontSize: '11px' }}>{label}</p>
      </div>
    )
  }
  return null
}

export function WeekChart({ data, goal }: WeekChartProps) {
  const todayStr = new Date().toISOString().split('T')[0]

  const chartData = data.map((d) => ({
    day: formatDate(d.date),
    calories: Math.round(d.calories),
    isToday: d.date === todayStr,
  }))

  return (
    <ResponsiveContainer width="100%" height={160}>
      <BarChart data={chartData} barCategoryGap="30%" margin={{ top: 8, right: 4, left: -20, bottom: 0 }}>
        <CartesianGrid vertical={false} stroke="var(--border-subtle)" strokeDasharray="3 3" />
        <XAxis
          dataKey="day"
          tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          tick={{ fill: 'var(--text-muted)', fontSize: 10 }}
          axisLine={false}
          tickLine={false}
        />
        <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(245,158,11,0.05)' }} />
        {goal > 0 && (
          <ReferenceLine
            y={goal}
            stroke="var(--red)"
            strokeDasharray="4 4"
            strokeWidth={1.5}
            opacity={0.7}
          />
        )}
        <Bar dataKey="calories" radius={[4, 4, 0, 0]}>
          {chartData.map((entry, idx) => (
            <Cell
              key={idx}
              fill={entry.isToday ? 'var(--accent)' : 'var(--border)'}
              opacity={entry.calories === 0 ? 0.3 : 1}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
