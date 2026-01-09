export interface FitcheckResponse {
  overall_vibe: {
    summary: string
    category: string
  }
  what_works: string[]
  what_needs_work: string[]
  suggestions: string[]
  item_flags: {
    dress: string
    top: string
    bottom: string
    shoes: string
    bag: string
    accessories: string
  }
}

export interface AppState {
  uploadedImage: File | null
  isAnalyzing: boolean
  showResults: boolean
  analysisData: FitcheckResponse | null
}
