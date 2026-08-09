import type { LucideIcon } from 'lucide-react'

interface KPICardProps {
  title: string
  value: number
  icon: LucideIcon
}

export function KPICard({ title, value, icon: Icon }: KPICardProps) {
  return (
    <div className="flex flex-col gap-2 rounded-2xl bg-white p-6 shadow-md dark:bg-gray-800">
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm font-medium text-gray-600 dark:text-gray-300">{title}</span>
        <span className="flex size-10 items-center justify-center rounded-xl bg-blue-50 text-primary dark:bg-blue-950/50 dark:text-blue-300">
          <Icon className="size-5" aria-hidden />
        </span>
      </div>
      <p className="text-4xl font-bold text-gray-900 dark:text-white">{value.toLocaleString()}</p>
      <p className="text-sm text-gray-500 dark:text-gray-400">Current records</p>
    </div>
  )
}
