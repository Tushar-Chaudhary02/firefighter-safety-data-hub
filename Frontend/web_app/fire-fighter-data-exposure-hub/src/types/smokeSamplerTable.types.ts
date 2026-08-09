export interface SmokeSamplerTableRow {
  sample_id: string
  submission_id: string
  user_id: string
  submission_created_at: string
  chemical_name: string
  percentage_proportion: number
}

export interface SmokeSamplerTableQueryParams {
  page: number
  pageSize: number
}
