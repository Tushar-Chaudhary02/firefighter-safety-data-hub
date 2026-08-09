import { createColumnHelper } from '@tanstack/react-table'
import type { SmokeSamplerTableRow } from '@/types/smokeSamplerTable.types'

const columnHelper = createColumnHelper<SmokeSamplerTableRow>()

function formatDate(iso: string) {
  const d = new Date(iso)
  return Number.isNaN(d.getTime()) ? iso : d.toLocaleString()
}

export const smokeSamplerColumns = [
  columnHelper.accessor('sample_id', { header: 'Sample ID', cell: (info) => info.getValue() }),
  columnHelper.accessor('submission_id', {
    header: 'Submission ID',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('user_id', { header: 'User ID', cell: (info) => info.getValue() }),
  columnHelper.accessor('submission_created_at', {
    header: 'Submission created',
    cell: (info) => formatDate(info.getValue()),
  }),
  columnHelper.accessor('chemical_name', {
    header: 'Chemical name',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('percentage_proportion', {
    header: 'Proportion (%)',
    cell: (info) => info.getValue(),
  }),
]
