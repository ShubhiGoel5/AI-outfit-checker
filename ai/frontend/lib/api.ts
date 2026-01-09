import type { FitcheckResponse } from "./types"

const API_BASE_URL = "http://localhost:8000"

export async function submitFitCheck(image: File): Promise<FitcheckResponse> {
  const formData = new FormData()
  formData.append("image", image)

  const response = await fetch(`${API_BASE_URL}/fitcheck`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    throw new Error("Fitcheck failed")
  }

  return response.json()
}
