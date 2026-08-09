export interface PPETableRow {
  ppe_id: string
  user_id: string
  event_id: string | null
  helmet_id: string
  hood_id: string
  face_mask_id: string
  scba_id: string
  glove_id: string
  boot_id: string
  bunker_coat_id: string
  bunker_pants_id: string
  is_ppe_updated: boolean
  created_at: string
}

export interface PPETableQueryParams {
  page: number
  pageSize: number
}
