import { useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { isAxiosError } from 'axios'
import { ROUTES } from '@/constants/routes'
import { queryKeys } from '@/constants/queryKeys'
import { useAuth } from '@/hooks/useAuth'
import { getSmokeSamplerTableData } from '@/api/smokeSamplerTable.api'
import { SmokeSamplerDataTable } from '@/features/smokeSamplerTable/SmokeSamplerDataTable'

export default function SmokeSamplerTablePage() {
  const { logout } = useAuth()

  const pingQuery = useQuery({
    queryKey: queryKeys.smokeSamplerTableData({ page: 1, pageSize: 1 }),
    queryFn: () => getSmokeSamplerTableData({ page: 1, pageSize: 1 }),
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
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Smoke sample Table</h1>
          <p className="mt-1 text-gray-600 dark:text-gray-400">
            Browse smoke sampler samples with submission metadata. Export the full dataset as CSV.
          </p>
        </div>
      </div>
      <SmokeSamplerDataTable />
    </div>
  )
}
