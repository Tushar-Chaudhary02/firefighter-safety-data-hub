import { axiosInstance } from '@/api/axiosInstance'
import type { PaginatedResponse } from '@/types/table.types'
import type { SmokeSamplerTableQueryParams, SmokeSamplerTableRow } from '@/types/smokeSamplerTable.types'

type LegacyResponse = {
  results?: SmokeSamplerTableRow[]
  count?: number
}

type SpecResponse = {
  data?: SmokeSamplerTableRow[]
  total?: number
}

export async function getSmokeSamplerTableData(
  params: SmokeSamplerTableQueryParams
): Promise<PaginatedResponse<SmokeSamplerTableRow>> {
  const { page, pageSize } = params

  const { data: raw } = await axiosInstance.get<LegacyResponse & SpecResponse>(
    '/table/smoke-sampler-data',
    {
      params: {
        page,
        limit: pageSize,
      },
    }
  )

  const rows = Array.isArray(raw.data)
    ? raw.data
    : Array.isArray(raw.results)
      ? raw.results
      : []

  const total = Number(raw.total ?? raw.count ?? rows.length)
  const totalPages = Math.max(1, Math.ceil(total / pageSize))

  return {
    data: rows,
    total,
    page,
    pageSize,
    totalPages,
  }
}

export async function downloadSmokeSamplerTableCSV(): Promise<void> {
  const response = await axiosInstance.get('/table/export-smoke-sampler-data', {
    responseType: 'blob',
  })
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'smoke-sampler-data.csv')
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}
