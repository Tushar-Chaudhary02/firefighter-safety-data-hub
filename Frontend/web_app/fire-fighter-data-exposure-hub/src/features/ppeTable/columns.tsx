import { createColumnHelper } from '@tanstack/react-table'
import type { PPETableRow } from '@/types/ppeTable.types'

const columnHelper = createColumnHelper<PPETableRow>()

export const ppeColumns = [
  columnHelper.accessor('ppe_id', { header: 'PPE ID', cell: (info) => info.getValue() }),
  columnHelper.accessor('user_id', { header: 'User ID', cell: (info) => info.getValue() }),
  columnHelper.accessor('event_id', {
    header: 'Event ID',
    cell: (info) => info.getValue() ?? '—',
  }),
  columnHelper.accessor('helmet_id', { header: 'Helmet', cell: (info) => info.getValue() }),
  columnHelper.accessor('hood_id', { header: 'Hood', cell: (info) => info.getValue() }),
  columnHelper.accessor('face_mask_id', { header: 'Face mask', cell: (info) => info.getValue() }),
  columnHelper.accessor('scba_id', { header: 'SCBA', cell: (info) => info.getValue() }),
  columnHelper.accessor('glove_id', { header: 'Gloves', cell: (info) => info.getValue() }),
  columnHelper.accessor('boot_id', { header: 'Boots', cell: (info) => info.getValue() }),
  columnHelper.accessor('bunker_coat_id', { header: 'Bunker coat', cell: (info) => info.getValue() }),
  columnHelper.accessor('bunker_pants_id', {
    header: 'Bunker pants',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('is_ppe_updated', {
    header: 'PPE updated',
    cell: (info) => (info.getValue() ? 'Yes' : 'No'),
  }),
  columnHelper.accessor('created_at', { header: 'Created', cell: (info) => info.getValue() }),
]
