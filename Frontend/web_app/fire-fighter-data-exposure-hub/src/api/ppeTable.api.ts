import { axiosInstance } from '@/api/axiosInstance'
import type { PaginatedResponse } from '@/types/table.types'
import type { PPETableQueryParams, PPETableRow } from '@/types/ppeTable.types'

type LegacyPPEResponse = {
  results?: PPETableRow[]
  count?: number
}

type SpecPPEResponse = {
  data?: PPETableRow[]
  total?: number
}

export async function getPPETableData(
  params: PPETableQueryParams
): Promise<PaginatedResponse<PPETableRow>> {
  const { page, pageSize } = params

  const { data: raw } = await axiosInstance.get<LegacyPPEResponse & SpecPPEResponse>(
    '/table/ppedata',
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

export async function downloadPPETableCSV(): Promise<void> {
  const response = await axiosInstance.get('/table/export-ppe-data', {
    responseType: 'blob',
  })
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'ppe-data.csv')
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}
