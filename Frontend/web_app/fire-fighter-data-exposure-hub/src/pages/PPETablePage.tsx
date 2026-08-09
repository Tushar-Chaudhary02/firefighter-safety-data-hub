import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { isAxiosError } from 'axios'
import { ROUTES } from '@/constants/routes'
import { queryKeys } from '@/constants/queryKeys'
import { useAuth } from '@/hooks/useAuth'
import { getPPETableData } from '@/api/ppeTable.api'
import { PPEDataTable } from '@/features/ppeTable/PPEDataTable'

export default function PPETablePage() {
  const { logout } = useAuth()

  const pingQuery = useQuery({
    queryKey: queryKeys.ppeTableData({ page: 1, pageSize: 1 }),
    queryFn: () => getPPETableData({ page: 1, pageSize: 1 }),
  })

  useEffect(() => {
    if (!pingQuery.isError || !pingQuery.error) return
    if (!isAxiosError(pingQuery.error)) return
    const status = pingQuery.error.response?.status
    if (status !== 401 && status !== 403) return
    logout()
    window.location.assign(ROUTES.error401)
  }, [pingQuery.isError, pingQuery.error, logout])

  return (
    <div>
      <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">PPE Table</h1>
          <p className="mt-1 text-gray-600 dark:text-gray-400">
            Browse paginated PPE records. Export the full dataset as CSV.
          </p>
        </div>
      </div>
      <PPEDataTable />
    </div>
  )
}
